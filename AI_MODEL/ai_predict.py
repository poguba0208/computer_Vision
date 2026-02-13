"""
공사장 안전모 감지 AI 모델 - 예측(추론) 스크립트
Google Colab에서 실행

학습된 모델(best.pt)로 이미지를 분석하여
헬멧 착용 여부를 JSON 형식으로 출력합니다.

클래스 매핑:
    0 → head (안전모 미착용)
    1 → helmet (안전모 착용)

위험 수준 판정:
    미착용 0%       → Safe
    미착용 1~30%    → Warning
    미착용 31% 이상 → Danger
"""

import json
from ultralytics import YOLO

# ============================================
# 1. 모델 로드
# ============================================
save_path = "/content/drive/MyDrive/My_YOLO_Project/safety_model6/weights/"
model = YOLO(save_path + "best.pt")
print("✅ 모델 로드 성공")
print("학습된 클래스 목록:", model.names)

# ============================================
# 2. 이미지 예측
# ============================================
image_path = "/content/sample_data/test1.jpg"  # 테스트 이미지 경로

results = model.predict(image_path, conf=0.2)

for result in results:
    boxes = result.boxes
    detected_classes = boxes.cls.int().tolist()

    # 클래스별 카운트
    head_count = detected_classes.count(0)      # 안전모 미착용
    helmet_count = detected_classes.count(1)    # 안전모 착용
    total_workers = head_count + helmet_count

    # ============================================
    # 3. 위험도 계산
    # ============================================
    risk_ratio = 0
    if total_workers > 0:
        risk_ratio = (head_count / total_workers) * 100

    # 위험 수준 판정
    status = "Safe"
    if risk_ratio > 0:
        status = "Warning"
    if risk_ratio > 30:
        status = "Danger"

    # ============================================
    # 4. JSON 결과 생성 (백엔드 전달 형식)
    # ============================================
    output_data = {
        "summary": {
            "total_workers": total_workers,
            "helmet_worn": helmet_count,
            "helmet_not_worn": head_count,
            "risk_percentage": round(risk_ratio, 2),
            "safety_status": status
        },
        "details": []
    }

    for box in boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])

        output_data["details"].append({
            "class": label,
            "confidence": round(conf, 2),
            "bbox": box.xyxy[0].tolist()
        })

    # 결과 출력
    print("--- 분석 결과 (JSON 형식) ---")
    print(json.dumps(output_data, indent=4, ensure_ascii=False))

    # 이미지에 바운딩박스 그려서 보기
    result.show()
