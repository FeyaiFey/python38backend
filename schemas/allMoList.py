from datetime import date
from pydantic import BaseModel,field_validator
from typing import Optional
from typing import List

class Allpackagelists(BaseModel):
    id:int
    order_id:Optional[str] = None
    item_code:Optional[str] = None
    item_name:Optional[str] = None
    package:Optional[str] = None
    package_remark:Optional[str] = None
    bonding:Optional[str] = None
    lot_code:Optional[str] = None
    loading_method:Optional[str] = None
    assy_step:Optional[str] = None
    cp_step:Optional[str] = None
    pgm_name:Optional[str] = None
    wire:Optional[str] = None
    business_qty:Optional[int] = None
    arrive_qty:Optional[int] = None
    order_date:Optional[date] = None
    last_arrival_date:Optional[date] = None
    complete_date:Optional[date] = None
    supply:Optional[str] = None
    status:Optional[str] = None
    remark:Optional[str] = None
    children:Optional[str] = None
    @field_validator("business_qty", mode="before")
    def ensure_integer_1(cls, v):
        if isinstance(v, float):
            return int(v)
        return v
    @field_validator("arrive_qty", mode="before")
    def ensure_integer_2(cls, v):
        if isinstance(v, float):
            return int(v)
        return v

class Allpackagelistsresponse(BaseModel):
    code:int
    data: List[Allpackagelists]
    total:int

class Allbom(BaseModel):
    id: int
    order_id: Optional[str] = None
    main_chip: Optional[str] = None
    bom_code: Optional[str] = None
    item_name: Optional[str] = None
    bom_lot: Optional[str] = None
    bom_business_qty: Optional[int] = None
    bom_second_qty: Optional[float] = None
    bom_wafer_id: Optional[str] = None

class Allbomresponse(BaseModel):
    code:int
    data: List[Allbom]