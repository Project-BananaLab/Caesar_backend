"""
Health Check API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db, get_db_info


router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    database: dict
    services: dict


@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """시스템 상태 체크"""
    try:
        # DB 연결 테스트
        db.execute("SELECT 1")
        db_status = "healthy"
        db_info = get_db_info()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        db_info = {"error": str(e)}

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": "1.0.0",
        "database": {"status": db_status, **db_info},
        "services": {
            "mcp_servers": "not_implemented",
            "rag": "not_implemented",
            "tools": "not_implemented",
        },
    }


@router.get("/ping")
async def ping():
    """간단한 ping 체크"""
    return {"message": "pong"}

