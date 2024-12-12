import os
from fastapi import APIRouter, Depends, HTTPException
from models.dbm_user import User
from api.users import get_current_user
from fastapi.responses import FileResponse
from typing import Optional
from core.config import settings


router = APIRouter()

public_folder = settings.UPLOAD_PUBLIC_FOLDER
root_folder = settings.ROOT_FOLDER

def get_folder_structure(path):
    folder_tree = []
    for item in os.listdir(path):
        item_path = path + "\\" + item
        if os.path.isdir(item_path):
            folder_tree.append({
                "name": item,
                "path": item_path[item_path.find("upload"):],
                "type":"folder",
                "children": get_folder_structure(item_path)
            })
        elif os.path.isfile(item_path):
            folder_tree.append({
                "name": item,
                "path": item_path[item_path.find("upload"):],
                "type":"file",
            })
    return folder_tree

def get_files(path):
    files = []
    for item in os.listdir(path):
        files.append({"name": item, "path": path + "\\" + item})
    return files


@router.get("/folder")
def get_folder(current_user: User = Depends(get_current_user)):
    try:
        folder_tree = get_folder_structure(public_folder)
        return {"code": 0, "data": folder_tree}
    except:
        raise HTTPException(status_code=400, detail="文件结构获取错误！")

@router.get("/filelists")
def get_filelist(path:Optional[str]=None,current_user: User = Depends(get_current_user)):
    try:
        files = get_files(root_folder + "\\" + path)
        return {"code": 0, "data": files}
    except:
        raise HTTPException(status_code=400, detail="文件结构获取错误！")


@router.get("/preview")
def get_file_path(path:Optional[str]=None,file_name :Optional[str]=None,current_user: User = Depends(get_current_user)):
    full_path = root_folder + "\\" + path
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="文件未找到!")
    return FileResponse(full_path, filename=file_name)


@router.get("/download")
async def get_file(path:Optional[str]=None,file_name :Optional[str]=None,current_user: User = Depends(get_current_user)):
    """
    获取文件的下载链接
    """
    full_path = root_folder + "\\" + path
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="文件未找到!")
    return FileResponse(full_path,filename=file_name)