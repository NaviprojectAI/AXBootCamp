from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import settings
from backend.database import init_db
from backend.api.routes import search, keywords, jobs, sheets

FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="나라장터 입찰공고 검색 시스템",
    description="나라장터 입찰공고를 키워드로 자동 검색하고 Google Sheets에 기록합니다.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["검색"])
app.include_router(keywords.router, prefix="/api/keywords", tags=["키워드"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["작업"])
app.include_router(sheets.router, prefix="/api/sheets", tags=["Sheets"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


# 프론트엔드 정적 파일 서빙
if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        return FileResponse(FRONTEND_DIR / "index.html")
