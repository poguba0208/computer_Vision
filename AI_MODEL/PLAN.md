# 공사장 헬멧 감지 웹 & 서버 구현 계획

## 개요
공사장 이미지를 업로드하면 사람을 인식하고 헬멧 착용 여부를 표시해주는 웹 애플리케이션.
AI 모델은 나중에 연결 예정이므로, **Mock(더미) 응답**으로 구조만 먼저 잡음.

## 기술 스택
- **Backend**: Python FastAPI (py 3.10)
- **Frontend**: React (Vite + TypeScript)
- **AI 연동**: 모델 연결 인터페이스만 준비 (나중에 실제 모델 교체)

## 프로젝트 구조
```
AI_MODEL/
├── backend/
│   ├── main.py              # FastAPI 서버 진입점
│   ├── requirements.txt     # Python 의존성
│   ├── routers/
│   │   └── detection.py     # /api/detect 엔드포인트
│   ├── services/
│   │   └── model_service.py # AI 모델 서비스 (Mock → 실제 모델 교체 지점)
│   └── uploads/             # 업로드 이미지 저장 폴더
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── src/
│   │   ├── App.tsx          # 메인 앱
│   │   ├── main.tsx         # 진입점
│   │   ├── components/
│   │   │   ├── ImageUploader.tsx   # 이미지 업로드 컴포넌트
│   │   │   ├── ResultDisplay.tsx   # 감지 결과 표시 (바운딩박스)
│   │   │   └── Header.tsx          # 상단 헤더
│   │   ├── types/
│   │   │   └── detection.ts # 타입 정의
│   │   └── styles/
│   │       └── App.css      # 스타일
│   └── vite.config.ts
└── PLAN.md
```

## 구현 단계

### Step 1: Backend (FastAPI 서버)
1. `requirements.txt` 작성 (fastapi, uvicorn, python-multipart, Pillow)
2. `main.py` - FastAPI 앱 생성, CORS 설정, 라우터 등록
3. `routers/detection.py` - POST `/api/detect` 엔드포인트
   - 이미지 파일 수신 → model_service 호출 → 결과 JSON 반환
4. `services/model_service.py` - Mock 감지 서비스
   - 나중에 실제 YOLO 모델로 교체할 수 있도록 인터페이스 설계
   - 현재는 더미 바운딩박스 + 헬멧 여부 반환

### Step 2: Frontend (React)
1. Vite + React + TypeScript 프로젝트 생성
2. `ImageUploader` - 드래그앤드롭 + 클릭 업로드
3. `ResultDisplay` - 원본 이미지 위에 바운딩박스 오버레이
   - 헬멧 착용: 초록색 박스 + "Helmet ✓"
   - 미착용: 빨간색 박스 + "No Helmet ✗"
4. 감지 통계 요약 (총 인원, 헬멧 착용, 미착용)

### Step 3: 연동
- Frontend → Backend API 호출 (fetch /api/detect)
- 결과 표시

## API 명세

### POST /api/detect
- **Request**: multipart/form-data, field: `file` (이미지)
- **Response**:
```json
{
  "success": true,
  "image_width": 1920,
  "image_height": 1080,
  "detections": [
    {
      "id": 1,
      "bbox": [x1, y1, x2, y2],
      "label": "helmet" | "no_helmet",
      "confidence": 0.95
    }
  ],
  "summary": {
    "total_persons": 5,
    "with_helmet": 3,
    "without_helmet": 2
  }
}
```

## 나중에 모델 연결 시
`services/model_service.py`의 `detect()` 함수만 실제 모델 추론 코드로 교체하면 됨.
