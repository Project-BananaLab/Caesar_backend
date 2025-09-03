"""
FastAPI Backend Main
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables
from .routers import users_router, logs_router, health_router


def create_app() -> FastAPI:
    """FastAPI 앱 생성 및 설정"""
    app = FastAPI(
        title="Caesar MCP Backend API",
        description="시저 팀 MCP 프로젝트 백엔드 API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 개발용, 프로덕션에서는 제한 필요
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(health_router)
    app.include_router(users_router)
    app.include_router(logs_router)

    # 시작 이벤트
    @app.on_event("startup")
    async def startup_event():
        print("FastAPI 서버 시작 중...")
        create_tables()
        print("백엔드 초기화 완료")

    # 종료 이벤트
    @app.on_event("shutdown")
    async def shutdown_event():
        print("FastAPI 서버 종료 중...")

    return app


# FastAPI 앱 인스턴스
app = create_app()


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Caesar MCP Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
