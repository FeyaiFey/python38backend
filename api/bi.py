from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.base import get_session
from models.dbm_user import User
from api.users import get_current_user
from crud.bi_caiwu import get_panel_data
from schemas.bi import CaiwuResponse


router = APIRouter()

@router.get('/caiwu',response_model=CaiwuResponse)
def caiwu(session: Session = Depends(get_session),current_user:User = Depends(get_current_user)):
    summary = get_panel_data(session)
    print(summary)
    return {"code":0,"data": summary}
