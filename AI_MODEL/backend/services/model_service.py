"""
헬멧 감지 모델 서비스

실제 YOLOv8 모델을 로드하여 추론합니다.
best.pt 파일을 backend/models/ 폴더에 넣어주세요.

클래스 매핑:
    0 → head (안전모 미착용)
    1 → helmet (안전모 착용)
"""

from pathlib import Path
from ultralytics import YOLO

# 모델 로드 (서버 시작 시 한 번만 로드)
MODEL_PATH = Path(__file__).parent.parent / "models" / "best.pt"

if MODEL_PATH.exists():
    model = YOLO(str(MODEL_PATH))
    print(f"✅ 모델 로드 성공: {MODEL_PATH}")
    print(f"   학습된 클래스: {model.names}")
else:
    model = None
    print(f"⚠️ 모델 파일 없음: {MODEL_PATH}")
    print(f"   best.pt 파일을 backend/models/ 폴더에 넣어주세요.")


def detect_helmets(image_path: str, width: int, height: int) -> dict:
    """
    이미지에서 헬멧 착용 여부를 감지합니다.

    Args:
        image_path: 이미지 파일 경로
        width: 이미지 너비
        height: 이미지 높이

    Returns:
        {
            "summary": { total_workers, helmet_worn, helmet_not_worn, risk_percentage, safety_status },
            "details": [ { class, confidence, bbox } ]
        }
    """
    if model is None:
        return {
            "summary": {
                "total_workers": 0,
                "helmet_worn": 0,
                "helmet_not_worn": 0,
                "risk_percentage": 0,
                "safety_status": "Error",
            },
            "details": [],
            "error": "모델 파일(best.pt)이 로드되지 않았습니다.",
        }

    # 모델 예측 실행
    results = model.predict(image_path, conf=0.2)

    details = []
    head_count = 0
    helmet_count = 0

    for result in results:
        boxes = result.boxes
        detected_classes = boxes.cls.int().tolist()

        head_count = detected_classes.count(0)    # 안전모 미착용
        helmet_count = detected_classes.count(1)  # 안전모 착용

        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            details.append({
                "class": label,
                "confidence": round(conf, 2),
                "bbox": box.xyxy[0].tolist(),
            })

    total_workers = head_count + helmet_count

    # 위험도 계산
    risk_ratio = 0
    if total_workers > 0:
        risk_ratio = (head_count / total_workers) * 100

    # 위험 수준 판정
    safety_status = "Safe"
    if risk_ratio > 0:
        safety_status = "Warning"
    if risk_ratio > 30:
        safety_status = "Danger"

    return {
        "summary": {
            "total_workers": total_workers,
            "helmet_worn": helmet_count,
            "helmet_not_worn": head_count,
            "risk_percentage": round(risk_ratio, 2),
            "safety_status": safety_status,
        },
        "details": details,
    }
