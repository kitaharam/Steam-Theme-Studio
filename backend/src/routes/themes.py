from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Theme
from ..schemas import ThemeCreate, ThemeUpdate, Theme as ThemeSchema
from ..crud import themes as crud

router = APIRouter()

@router.get("/", response_model=List[ThemeSchema])
async def list_themes(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取主题列表"""
    return await crud.get_themes(db, skip=skip, limit=limit)

@router.post("/", response_model=ThemeSchema)
async def create_theme(
    theme: ThemeCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新主题"""
    db_theme = await crud.get_theme_by_name(db, name=theme.name)
    if db_theme:
        raise HTTPException(status_code=400, detail="主题名称已存在")
    return await crud.create_theme(db=db, theme=theme)

@router.get("/{theme_id}", response_model=ThemeSchema)
async def get_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取特定主题"""
    db_theme = await crud.get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    return db_theme

@router.put("/{theme_id}", response_model=ThemeSchema)
async def update_theme(
    theme_id: int,
    theme: ThemeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新主题"""
    db_theme = await crud.get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    return await crud.update_theme(db=db, theme_id=theme_id, theme=theme)

@router.delete("/{theme_id}")
async def delete_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除主题"""
    db_theme = await crud.get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    await crud.delete_theme(db=db, theme_id=theme_id)
    return {"ok": True} 