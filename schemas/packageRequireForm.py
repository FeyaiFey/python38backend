from datetime import date,datetime
import uuid
from pydantic import BaseModel
from typing import Optional
from typing import List


class Allpackagerequirelists(BaseModel):
    require_id: uuid.UUID
    require_date: date
    item_name: str
    qty: int
    sales: str
    emergency: Optional[str] = None
    remark1: Optional[str] = None
    remark2: Optional[str] = None
    status: bool
    order_id: Optional[str] = None
    modified_date: datetime
    submit_role: str

class Allpackagerequirelistsresponse(BaseModel):
    code:int
    data: List[Allpackagerequirelists]
    total:int