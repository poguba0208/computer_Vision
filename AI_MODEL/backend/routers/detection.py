import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image

from services.model_service import detect_helmets

router = APIRouter()

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    # 확장자 검증
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"허용되지 않는 파일 형식입니다. 허용: {ALLOWED_EXTENSIONS}")

    # 파일 읽기
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "파일 크기가 10MB를 초과합니다.")

    # 고유 파일명으로 저장
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOADS_DIR / filename
    filepath.write_bytes(contents)

    # 이미지 크기 확인
    try:
        img = Image.open(filepath)
        width, height = img.size
    except Exception:
        filepath.unlink(missing_ok=True)
        raise HTTPException(400, "이미지 파일을 열 수 없습니다.")

    # 모델 추론
    result = detect_helmets(str(filepath), width, height)

    return {
        "success": True,
        "image_url": f"/uploads/{filename}",
        "image_width": width,
        "image_height": height,
        "summary": result["summary"],
        "details": result["details"],
    }
