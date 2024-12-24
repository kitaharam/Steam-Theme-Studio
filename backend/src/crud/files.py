from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ThemeFile
from ..schemas import ThemeFileCreate, ThemeFileUpdate

async def get_theme_file(db: AsyncSession, file_id: int):
    """获取特定文件"""
    result = await db.execute(select(ThemeFile).filter(ThemeFile.id == file_id))
    return result.scalar_one_or_none()

async def get_theme_files(db: AsyncSession, theme_id: int):
    """获取主题的所有文件"""
    result = await db.execute(
        select(ThemeFile).filter(ThemeFile.theme_id == theme_id)
    )
    return result.scalars().all()

async def create_theme_file(db: AsyncSession, file: ThemeFileCreate):
    """创建新文件"""
    db_file = ThemeFile(**file.model_dump())
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file

async def update_theme_file(db: AsyncSession, file_id: int, file: ThemeFileUpdate):
    """更新文件"""
    db_file = await get_theme_file(db, file_id)
    if db_file:
        file_data = file.model_dump(exclude_unset=True)
        for key, value in file_data.items():
            setattr(db_file, key, value)
        await db.commit()
        await db.refresh(db_file)
    return db_file

async def delete_theme_file(db: AsyncSession, file_id: int):
    """删除文件"""
    db_file = await get_theme_file(db, file_id)
    if db_file:
        await db.delete(db_file)
        await db.commit()
    return db_file 