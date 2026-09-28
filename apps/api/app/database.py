import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def database_url() -> str:
    # SQLite keeps local development friction-free; Render uses DATABASE_URL from Neon.
    url = os.getenv("DATABASE_URL", "sqlite:///./bridge_lifecycle.sqlite3")
    return url.replace("postgresql://", "postgresql+psycopg://", 1)


engine = create_engine(database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass
