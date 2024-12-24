from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./steam_theme_studio.db"
    
    # 应用配置
    APP_NAME: str = "Steam Theme Studio"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # 路径配置
    BASE_DIR: Path = Path(__file__).parent.parent
    MILLENNIUM_PATH: Path = BASE_DIR / "millennium"
    THEMES_PATH: Path = BASE_DIR / "themes"
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # WebSocket配置
    WS_HEARTBEAT_INTERVAL: int = 30  # 秒
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    
    # 确保必要的目录存在
    settings.THEMES_PATH.mkdir(parents=True, exist_ok=True)
    settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    return settings 