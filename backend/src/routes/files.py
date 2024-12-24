from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import ThemeFile
from ..schemas import ThemeFileCreate, ThemeFileUpdate, ThemeFile as ThemeFileSchema
from ..crud import files as crud

router = APIRouter()

@router.get("/", response_model=List[ThemeFileSchema])
async def list_files(
    theme_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取主题的所有文件"""
    return await crud.get_theme_files(db, theme_id=theme_id)

@router.post("/", response_model=ThemeFileSchema)
async def create_file(
    file: ThemeFileCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新文件"""
    return await crud.create_theme_file(db=db, file=file)

@router.get("/{file_id}", response_model=ThemeFileSchema)
async def get_file(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取特定文件"""
    db_file = await crud.get_theme_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="文件不存在")
    return db_file

@router.put("/{file_id}", response_model=ThemeFileSchema)
async def update_file(
    file_id: int,
    file: ThemeFileUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新文件"""
    db_file = await crud.get_theme_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="文件不存在")
    return await crud.update_theme_file(db=db, file_id=file_id, file=file)

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除文件"""
    db_file = await crud.get_theme_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="文件不存在")
    await crud.delete_theme_file(db=db, file_id=file_id)
    return {"ok": True} 