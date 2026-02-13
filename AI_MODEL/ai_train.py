"""
공사장 안전모 감지 AI 모델 - 학습 스크립트
Google Colab에서 실행

사용법:
    1. Google Colab에서 이 파일 내용을 셀 단위로 실행
    2. 학습 완료 후 best.pt 파일을 backend/models/ 에 복사
"""

# ============================================
# 1. 패키지 설치
# ============================================
# !pip install ultralytics
# !pip install roboflow

# ============================================
# 2. Google Drive 연결
# ============================================
from google.colab import drive
drive.mount('/content/drive')

# ============================================
# 3. 데이터셋 다운로드 (Roboflow)
# ============================================
from roboflow import Roboflow

rf = Roboflow(api_key="F3TMlUjqXNTmAgwxdo3t")
project = rf.workspace("muncho02").project("hard-hat-sfsaw-udlfp")
version = project.version(2)
dataset = version.download("yolov8")

# ============================================
# 4. GPU 확인
# ============================================
import torch
print(f"GPU 사용 가능: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU 이름: {torch.cuda.get_device_name(0)}")

# ============================================
# 5. 모델 학습
# ============================================
from ultralytics import YOLO

# YOLOv8 Nano 모델 (전이학습)
model = YOLO("yolov8n.pt")

# 학습 실행
model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=30,          # 학습 반복 횟수
    imgsz=640,          # 이미지 크기
    augment=True,       # 데이터 증강 활성화
    mixup=0.2,          # 두 이미지를 겹쳐서 보여주는 기법
    degrees=10.0,       # 사진을 살짝 회전시켜서 학습
    project="/content/drive/MyDrive/My_YOLO_Project",
    name="safety_model"
)

# ============================================
# 6. 학습된 모델 확인 및 로드
# ============================================
import os

save_path = "/content/drive/MyDrive/My_YOLO_Project/safety_model6/weights/"

if os.path.exists(save_path + "best.pt"):
    print("✅ best.pt 파일이 드라이브에 안전하게 저장되어 있습니다!")
    print("파일 목록:", os.listdir(save_path))
else:
    print("❌ 파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.")

# 모델 로드
try:
    model = YOLO(save_path + "best.pt")
    print("✅ 모델 로드 성공")
    print("학습된 클래스 목록:", model.names)
except Exception as e:
    print(f"❌ 모델 로드 실패: {e}")
