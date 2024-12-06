from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date,datetime
import uuid

class PackageRequireFormLists(SQLModel, table=True):
    __tablename__ = 'HSUN_PACKAGE_REQUIRE_LIST'
    require_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4,  # 自动生成 UUID
        primary_key=True)
    require_date:date = Field(nullable=False)
    item_name: str = Field(nullable=False)
    qty: int = Field(nullable=False)
    sales:str = Field(nullable=False)
    emergency:str = Field(nullable=True)
    remark1:str = Field(nullable=True)
    remark2:str = Field(nullable=True)
    status:bool = Field(default=False, nullable=False)
    order_id:str = Field(nullable=True)
    modified_date:Optional[datetime] = Field(default_factory=datetime.now, nullable=True)
    submit_role:str = Field(nullable=True)

