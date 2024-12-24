from fastapi import APIRouter
from typing import Dict
from ..config import get_settings

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()

@router.get("")
async def health_check() -> Dict[str, str]:
    """
    健康检查接口
    返回应用基本信息和状态
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    简单的ping测试
    用于验证API是否响应
    """
    return {"ping": "pong"} 