from sqlmodel import Session, select
from models.dbm_routes import Routes
from models.dbm_user import User
from schemas.user import UserCreate,UserRead
from core.security import get_password_hash, verify_password
from fastapi import Depends
from database.base import get_session


def create_user(user: UserCreate, session: Session = Depends(get_session)):  # UserCreate 是前端传给后端的数据
    hashed_password = get_password_hash(user.password)
    if user.code == 68241373:
        new_user = User(email=user.email, username=user.username, hashed_password=hashed_password,role_id=1,file_name="avatar/avatar.jpg")   # 与后端数据库建立映射
    else:
        new_user = User(email=user.email, username=user.username, hashed_password=hashed_password,role_id=2,file_name="avatar/avatar.jpg")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def create_routes(session,role_id):
    query = select(Routes).where(Routes.role_id.contains(role_id))
    permissions = session.exec(query).all()
    if permissions:
        return permissions
    else:
        return None