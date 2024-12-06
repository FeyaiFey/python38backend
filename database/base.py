"""
创建数据库引擎和 SessionLocal
"""

from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 数据库会话的依赖项
def get_session():
    with Session(engine) as session:
        yield session