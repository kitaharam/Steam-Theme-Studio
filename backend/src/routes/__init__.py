from fastapi import APIRouter
from .themes import router as themes_router
from .files import router as files_router
from .millennium import router as millennium_router
from .health import router as health_router

api_router = APIRouter(prefix="/api")

api_router.include_router(themes_router, prefix="/themes", tags=["themes"])
api_router.include_router(files_router, prefix="/files", tags=["files"])
api_router.include_router(millennium_router, prefix="/millennium", tags=["millennium"])
api_router.include_router(health_router) 