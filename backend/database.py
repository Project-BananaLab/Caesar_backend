"""
Database 설정 - SQLite/PostgreSQL 지원
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# 환경 변수에서 DB 설정 읽기
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./caesar.db")
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite 또는 postgresql

# SQLite용 엔진 설정
if DATABASE_TYPE == "sqlite":
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL용 엔진 설정
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """테이블 생성"""
    Base.metadata.create_all(bind=engine)
    print(f"데이터베이스 테이블 생성 완료 ({DATABASE_TYPE})")


def get_db_info():
    """데이터베이스 정보 반환"""
    return {
        "type": DATABASE_TYPE,
        "url": DATABASE_URL,
        "tables": list(Base.metadata.tables.keys()),
    }

