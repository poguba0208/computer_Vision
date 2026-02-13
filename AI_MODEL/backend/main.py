from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from routers import detection

app = FastAPI(title="Helmet Detection API", version="1.0.0")

# CORS 설정 - 프론트엔드 개발 서버 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 폴더 생성
uploads_dir = Path(__file__).parent / "uploads"
uploads_dir.mkdir(exist_ok=True)

# 업로드된 이미지 정적 서빙
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# 라우터 등록
app.include_router(detection.router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Helmet Detection API is running"}
