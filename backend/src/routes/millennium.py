from fastapi import APIRouter, WebSocket, HTTPException, Depends
from pathlib import Path
from typing import List, Dict, Any
from ..millennium.core import MillenniumCore
from ..millennium.preview import ThemePreview
from ..config import get_settings

router = APIRouter(prefix="/api/millennium")
core = MillenniumCore()
preview_manager = None

def get_preview_manager():
    global preview_manager
    if preview_manager is None and core.steam_path:
        preview_manager = ThemePreview(core.steam_path)
    return preview_manager

@router.post("/initialize")
async def initialize_millennium():
    """初始化Millennium"""
    try:
        await core.initialize()
        return {"status": "success", "message": "Millennium初始化成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/themes")
async def list_themes() -> List[Dict[str, Any]]:
    """获取主题列表"""
    try:
        themes = await core.list_themes()
        return themes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/themes")
async def create_theme(name: str, config: Dict[str, Any]):
    """创建新主题"""
    try:
        theme_path = await core.create_theme(name, config)
        return {"status": "success", "path": str(theme_path)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/themes/{theme_name}")
async def get_theme(theme_name: str):
    """获取主题信息"""
    try:
        theme = await core.get_theme(theme_name)
        return theme
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/themes/{theme_name}")
async def update_theme(theme_name: str, config: Dict[str, Any]):
    """更新主题"""
    try:
        await core.update_theme(theme_name, config)
        return {"status": "success", "message": "主题更新成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/themes/{theme_name}")
async def delete_theme(theme_name: str):
    """删除主题"""
    try:
        await core.delete_theme(theme_name)
        return {"status": "success", "message": "主题删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/themes/{theme_name}/apply")
async def apply_theme(theme_name: str):
    """应用主题"""
    try:
        theme_path = core.themes_path / theme_name
        await core.apply_theme(theme_path)
        return {"status": "success", "message": "主题应用成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/themes/{theme_name}/preview")
async def start_preview(theme_name: str):
    """开始预览主题"""
    preview = get_preview_manager()
    if not preview:
        raise HTTPException(status_code=500, detail="Steam未安装或预览服务未初始化")

    try:
        theme_path = core.themes_path / theme_name
        await preview.preview_theme(theme_path)
        return {"status": "success", "message": "预览开始"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/themes/{theme_name}/preview")
async def stop_preview(theme_name: str):
    """停止预览主题"""
    preview = get_preview_manager()
    if not preview:
        return {"status": "success", "message": "预览服务未运行"}

    try:
        await preview.stop_preview()
        return {"status": "success", "message": "预览停止"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.websocket("/themes/{theme_name}/preview/ws")
async def preview_websocket(websocket: WebSocket, theme_name: str):
    """WebSocket连接用于实时预览"""
    preview = get_preview_manager()
    if not preview:
        await websocket.close(code=1000, reason="Steam未安装或预览服务未初始化")
        return

    await websocket.accept()
    try:
        await preview.handle_websocket(websocket)
    except Exception as e:
        await websocket.close(code=1000, reason=str(e))
    finally:
        await preview.stop_preview() 