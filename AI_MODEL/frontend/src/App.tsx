import { useState } from "react";
import Header from "./components/Header";
import ImageUploader from "./components/ImageUploader";
import ResultDisplay from "./components/ResultDisplay";
import type { DetectionResult } from "./types/detection";

export default function App() {
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/api/detect", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || `서버 오류 (${res.status})`);
      }

      const data: DetectionResult = await res.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Header />
      <main className="main">
        <ImageUploader onUpload={handleUpload} isLoading={isLoading} />
        {error && <div className="error-msg">{error}</div>}
        {result && <ResultDisplay result={result} />}
      </main>
    </div>
  );
}
