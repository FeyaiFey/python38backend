"""
数据库初始化脚本
"""
from sqlmodel import SQLModel
from database.base import engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)