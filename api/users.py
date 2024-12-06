from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.base import get_session
from models.dbm_user import User
from schemas.user import UserInfoResponse,Base64Image
from core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import os
from uuid import uuid4
import base64
import imghdr
import time


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 头像文件地址
AVATAR_FOLDER = "./upload/static/avatar"
os.makedirs(AVATAR_FOLDER, exist_ok=True)

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    name = decode_access_token(token)
    if not name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.query(User).filter(User.username == name).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/me",response_model=UserInfoResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    user_info = current_user.model_dump()
    # 添加一个新键值
    user_info["file_url"] = "http://192.168.168.67/api/static/"+user_info["file_name"]+f"?t={int(time.time())}"
    return {"code":0, "data":user_info}


@router.post("/upload-avatar/")
async def upload_avatar(image_data: Base64Image,current_user:User = Depends(get_current_user),session: Session = Depends(get_session)):
    base64_str = image_data.base64

    # 验证 Base64 数据是否包含前缀
    if "," not in base64_str:
        raise HTTPException(status_code=400, detail="Invalid Base64 format")

    # 分离前缀和数据
    prefix, base64_str = base64_str.split(",", 1)

    # 检查前缀中的 MIME 类型
    if "image/jpeg" in prefix:
        file_extension = "jpg"
    elif "image/png" in prefix:
        file_extension = "png"
    else:
        raise HTTPException(status_code=400, detail="Only JPG and PNG images are allowed")

    try:
        # 解码 Base64 数据
        file_data = base64.b64decode(base64_str)
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid Base64 data")

    # 验证文件内容是否为有效的图片
    file_type = imghdr.what(None, h=file_data)
    if file_type not in ["jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

    # 生成唯一文件名
    file_name = f"{uuid4().hex}.{file_extension}"
    file_path = os.path.join(AVATAR_FOLDER, file_name)

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(file_data)

    # 更新数据库中当前用户的 file_name 字段
    db_user = session.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        return {"code": 400}

    db_user.file_name = f"avatar/{file_name}"  # 更新字段
    session.commit()  # 提交更改
    # 返回文件路径
    return {"file_name": f"avatar/{file_name}"}




@router.get("/get-avatar/")
async def get_avatar(file_name: str):
    file_path = f"http://192.168.168.67/api/static/{file_name}?t={int(time.time())}"
    return {"code":0,"data": file_path}