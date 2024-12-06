from pydantic import BaseModel
from typing import Optional,List

class FileFolders(BaseModel):
    name:str
    type:str
    children:Optional[list] = None
    path:Optional[str] = None

class FileFoldersResponse(BaseModel):
    code:int
    data: List[FileFolders]