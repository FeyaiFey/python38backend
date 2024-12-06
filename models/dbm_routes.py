from sqlmodel import SQLModel, Field

class Routes(SQLModel, table=True):
    __tablename__ = "hsun-roles-permission"
    id: int = Field(primary_key=True)
    role_id: str = Field(nullable=False)
    api: str = Field(nullable=False)