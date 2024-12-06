from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_session
from models.dbm_user import User
from schemas.user import UserCreate, LoginResponse,UserLogin
from schemas.routes import RoutesResponse
from core.security import verify_password,create_access_token
from utils.email_validator import validate_email
from crud.user import create_user,create_routes
from sqlalchemy.exc import IntegrityError
from api.users import get_current_user
import time

router = APIRouter()


@router.post("/register", response_model=LoginResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):  # 前端传回的user
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="邮箱格式有误！")
    try:
        new_user = create_user(user, session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="用户已存在,请直接登录!")
    except Exception as e:
        raise HTTPException(status_code=400, detail="未知错误！")
    access_token = create_access_token(data={"sub": new_user.username})
    default_avatar_url = f"http://192.168.168.67/api/static/avatar/avatar.jpg?t={int(time.time())}"
    return {'code':0, 'data': {'id':new_user.id,'email':new_user.email,'username':new_user.username,'role_id':new_user.role_id,'file_name':'avatar/avatar.jpg','file_url':default_avatar_url}, "tokeninfo": {'access_token': access_token,'token_type':'bearer'}}


@router.post("/login", response_model=LoginResponse)
def login_user(userlogin:UserLogin, session: Session = Depends(get_session)):
    if not validate_email(userlogin.email):
        raise HTTPException(status_code=400, detail="邮箱格式有误！")
    user = session.query(User).filter(User.email == userlogin.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在！")
    elif not verify_password(userlogin.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="输入密码有误！")

    access_token = create_access_token(data={"sub": user.username})
    avatar_url = f"http://192.168.168.67/api/static/{user.file_name}?t={int(time.time())}"
    return { 'code':0, 'data': {'id':user.id,'email':user.email,'username':user.username,'role_id':user.role_id,'file_name':user.file_name,'file_url':avatar_url}, "tokeninfo": {'access_token': access_token,'token_type':'bearer'}}

@router.get("/logout")
def logout():
    return {'code':0,'data': "success"}

@router.get("/route",response_model=RoutesResponse)
def get_routes(session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    role_id = current_user.role_id
    routes = create_routes(session,role_id)
    return {'code':0,'data': routes}
