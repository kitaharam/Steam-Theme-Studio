from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ThemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    author: str
    version: str

class ThemeCreate(ThemeBase):
    pass

class ThemeUpdate(ThemeBase):
    name: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None

class Theme(ThemeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ThemeFileBase(BaseModel):
    theme_id: int
    file_path: str
    file_type: str
    content: str

class ThemeFileCreate(ThemeFileBase):
    pass

class ThemeFileUpdate(ThemeFileBase):
    theme_id: Optional[int] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    content: Optional[str] = None

class ThemeFile(ThemeFileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 