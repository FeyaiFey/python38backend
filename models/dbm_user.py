from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    __tablename__ = "hsun-users"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,  # 自动生成 UUID
        primary_key=True
    )
    email:str
    hashed_password:str
    username:str
    role_id:int
    file_name:str
