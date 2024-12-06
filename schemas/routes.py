from typing import List

from pydantic import BaseModel


class Routes(BaseModel):
    api:str

class RoutesResponse(BaseModel):
    code:int
    data:List[Routes]