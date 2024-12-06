from pydantic import BaseModel
from typing import List


class CaiwuDate(BaseModel):
    MONTH:str
    qty:int
    amount:float
    price:float

class CaiwuResponse(BaseModel):
    code:int
    data:List[CaiwuDate]