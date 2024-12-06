import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional,List


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    code:Optional[int] = None
    file_name:Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    role_id:int
    file_name: str
    file_url:str


class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    code:int
    data:UserRead
    tokeninfo:Token

class UserInfoResponse(BaseModel):
    code: int
    data: UserRead

# 请求体模型
class Base64Image(BaseModel):
    base64: str  # 接收 Base64 数据