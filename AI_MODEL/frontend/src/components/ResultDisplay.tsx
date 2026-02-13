import { useRef, useEffect, useState } from "react";
import type { DetectionResult, SafetyStatus } from "../types/detection";

interface Props {
  result: DetectionResult;
}

const STATUS_CONFIG: Record<SafetyStatus, { label: string; emoji: string; className: string }> = {
  Safe:    { label: "Safety Check - All Clear", emoji: "", className: "status-safe" },
  Warning: { label: "No Helmet Detected - Warning", emoji: "", className: "status-warning" },
  Danger:  { label: "No Helmet Detected - Danger", emoji: "", className: "status-danger" },
  Error:   { label: "Detection Error", emoji: "", className: "status-error" },
};

export default function ResultDisplay({ result }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [imageLoaded, setImageLoaded] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;

      // 원본 이미지 그리기
      ctx.drawImage(img, 0, 0);

      // 바운딩박스 그리기
      result.details.forEach((det) => {
        const [x1, y1, x2, y2] = det.bbox;
        const w = x2 - x1;
        const h = y2 - y1;

        const isHelmet = det.class === "helmet";
        const color = isHelmet ? "#22c55e" : "#ef4444";

        // 박스
        ctx.strokeStyle = color;
        ctx.lineWidth = Math.max(2, Math.min(canvas.width, canvas.height) * 0.003);
        ctx.strokeRect(x1, y1, w, h);

        // 라벨 배경
        const labelText = isHelmet
          ? `Helmet ${(det.confidence * 100).toFixed(0)}%`
          : `No Helmet ${(det.confidence * 100).toFixed(0)}%`;
        const fontSize = Math.max(12, Math.min(canvas.width, canvas.height) * 0.018);
        ctx.font = `bold ${fontSize}px sans-serif`;
        const textMetrics = ctx.measureText(labelText);
        const textHeight = fontSize + 4;
        const textWidth = textMetrics.width + 8;

        ctx.fillStyle = color;
        ctx.fillRect(x1, y1 - textHeight, textWidth, textHeight);

        ctx.fillStyle = "#ffffff";
        ctx.fillText(labelText, x1 + 4, y1 - 4);
      });

      setImageLoaded(true);
    };
    img.src = result.image_url;
  }, [result]);

  const { summary } = result;
  const statusInfo = STATUS_CONFIG[summary.safety_status] || STATUS_CONFIG.Error;

  return (
    <div className="result">
      {/* 안전 상태 배너 */}
      <div className={`status-banner ${statusInfo.className}`}>
        <span className="status-emoji">{statusInfo.emoji}</span>
        <span className="status-text">{statusInfo.label}</span>
        <span className="status-risk">Risk: {summary.risk_percentage}%</span>
      </div>

      <div className="result-body">
        <div className="result-image">
          <canvas ref={canvasRef} style={{ display: imageLoaded ? "block" : "none" }} />
          {!imageLoaded && <div className="spinner" />}
        </div>

        <div className="summary">
          <h3>Detection Summary</h3>
          <div className="summary-cards">
            <div className="card card-total">
              <span className="card-number">{summary.total_workers}</span>
              <span className="card-label">Total Workers</span>
            </div>
            <div className="card card-safe">
              <span className="card-number">{summary.helmet_worn}</span>
              <span className="card-label">Helmet On</span>
            </div>
            <div className="card card-danger">
              <span className="card-number">{summary.helmet_not_worn}</span>
              <span className="card-label">No Helmet</span>
            </div>
          </div>

          {/* 위험도 바 */}
          <div className="risk-bar-container">
            <div className="risk-bar-label">
              <span>Risk Level</span>
              <span>{summary.risk_percentage}%</span>
            </div>
            <div className="risk-bar-bg">
              <div
                className={`risk-bar-fill ${statusInfo.className}`}
                style={{ width: `${Math.min(summary.risk_percentage, 100)}%` }}
              />
            </div>
          </div>

          <div className="detection-list">
            <h4>Detail List</h4>
            {result.details
              .filter((d) => d.class === "helmet" || d.class === "head")
              .map((det, i) => (
                <div
                  key={i}
                  className={`det-item ${det.class === "helmet" ? "safe" : "danger"}`}
                >
                  <span className="det-label">
                    {det.class === "helmet" ? "Helmet" : "No Helmet"}
                  </span>
                  <span className="det-conf">{(det.confidence * 100).toFixed(1)}%</span>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}
