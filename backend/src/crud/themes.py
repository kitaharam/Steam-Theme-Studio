from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Theme
from ..schemas import ThemeCreate, ThemeUpdate

async def get_theme(db: AsyncSession, theme_id: int):
    """获取特定主题"""
    result = await db.execute(select(Theme).filter(Theme.id == theme_id))
    return result.scalar_one_or_none()

async def get_theme_by_name(db: AsyncSession, name: str):
    """通过名称获取主题"""
    result = await db.execute(select(Theme).filter(Theme.name == name))
    return result.scalar_one_or_none()

async def get_themes(db: AsyncSession, skip: int = 0, limit: int = 10):
    """获取主题列表"""
    result = await db.execute(select(Theme).offset(skip).limit(limit))
    return result.scalars().all()

async def create_theme(db: AsyncSession, theme: ThemeCreate):
    """创建新主题"""
    db_theme = Theme(**theme.model_dump())
    db.add(db_theme)
    await db.commit()
    await db.refresh(db_theme)
    return db_theme

async def update_theme(db: AsyncSession, theme_id: int, theme: ThemeUpdate):
    """更新主题"""
    db_theme = await get_theme(db, theme_id)
    if db_theme:
        theme_data = theme.model_dump(exclude_unset=True)
        for key, value in theme_data.items():
            setattr(db_theme, key, value)
        await db.commit()
        await db.refresh(db_theme)
    return db_theme

async def delete_theme(db: AsyncSession, theme_id: int):
    """删除主题"""
    db_theme = await get_theme(db, theme_id)
    if db_theme:
        await db.delete(db_theme)
        await db.commit()
    return db_theme 