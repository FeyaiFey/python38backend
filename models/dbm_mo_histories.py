from sqlmodel import SQLModel, Field
from datetime import date

class AllPackageLists(SQLModel, table=True):
    __tablename__ = 'XXF_VIEW_ALL_MO'
    id:int= Field(default=None, primary_key=True, nullable=False)
    order_id:str = Field(nullable=True)
    item_code:str = Field(nullable=True)
    item_name:str = Field(nullable=True)
    package:str = Field(nullable=True)
    package_remark:str = Field(nullable=True)
    bonding:str = Field(nullable=True)
    lot_code:str = Field(nullable=True)
    loading_method:str = Field(nullable=True)
    assy_step:str = Field(nullable=True)
    cp_step:str = Field(nullable=True)
    pgm_name:str = Field(nullable=True)
    wire:str = Field(nullable=True)
    business_qty:int = Field(default=None, nullable=True)
    arrive_qty:int = Field(default=None, nullable=True)
    order_date:date = Field(nullable=True)
    last_arrival_date:date = Field(nullable=True)
    complete_date:date = Field(nullable=True)
    supply:str = Field(nullable=True)
    status:str = Field(nullable=True)
    remark:str = Field(nullable=True)
    children:str = Field(nullable=True)

class AllBomLists(SQLModel, table=True):
    __tablename__ = 'XXF_VIEW_ALL_BOM'
    id:int= Field(default=None, primary_key=True, nullable=False)
    order_id:str = Field(nullable=True)
    main_chip:str = Field(nullable=True)
    bom_code:str = Field(nullable=True)
    item_name:str = Field(nullable=True)
    bom_lot: str = Field(nullable=True)
    bom_business_qty: int = Field(default=None, nullable=True)
    bom_second_qty: float = Field(default=None, nullable=True)
    bom_wafer_id: str = Field(nullable=True)
