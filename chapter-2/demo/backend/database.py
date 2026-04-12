from sqlmodel import SQLModel, create_engine, Session

from backend.config import settings

# DB 종류에 따라 엔진 설정 분기
connect_args = {}
if settings.database_url.startswith("sqlite"):
    from pathlib import Path

    db_path = settings.database_url.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True,
)


def init_db():
    """테이블 생성 및 기본 키워드 초기화"""
    # 모델 임포트 (테이블 등록용)
    from backend.models.bid import BidAnnouncement  # noqa: F401
    from backend.models.search_job import SearchJob  # noqa: F401
    from backend.models.keyword import Keyword  # noqa: F401

    SQLModel.metadata.create_all(engine)

    # 기본 키워드 초기화
    with Session(engine) as session:
        from sqlmodel import select

        existing = session.exec(select(Keyword)).first()
        if existing is None:
            for word in settings.default_keywords:
                session.add(Keyword(word=word, is_active=True))
            session.commit()


def get_session():
    """FastAPI 의존성 주입용 세션"""
    with Session(engine) as session:
        yield session
