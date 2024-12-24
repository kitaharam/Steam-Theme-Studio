import asyncio
from pathlib import Path
import websockets
import json
import shutil
import tempfile
from typing import Optional, Dict, Any
from .core import MillenniumCore

class ThemePreview:
    def __init__(self, steam_path: Path):
        self.steam_path = steam_path
        self.preview_path = Path(tempfile.mkdtemp())
        self.core = MillenniumCore()
        self.current_theme: Optional[Path] = None
        self.preview_active = False
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None

    async def preview_theme(self, theme_path: Path) -> None:
        """开始预览主题"""
        if not await self.core.validate_theme(theme_path):
            raise ValueError("无效的主题")

        self.current_theme = theme_path
        self.preview_active = True

        # 复制主题到临时目录
        preview_theme_path = self.preview_path / theme_path.name
        if preview_theme_path.exists():
            shutil.rmtree(preview_theme_path)
        shutil.copytree(theme_path, preview_theme_path)

        # 应用预览主题
        try:
            await self.core.apply_theme(preview_theme_path, is_preview=True)
        except Exception as e:
            self.preview_active = False
            raise Exception(f"应用预览主题失败: {str(e)}")

    async def update_preview(self, css_content: str) -> Dict[str, Any]:
        """更新预览CSS"""
        if not self.preview_active or not self.current_theme:
            return {"status": "error", "message": "预览未激活"}

        try:
            preview_theme_path = self.preview_path / self.current_theme.name
            webkit_css_path = preview_theme_path / "webkit.css"

            # 更新CSS文件
            with webkit_css_path.open("w", encoding="utf-8") as f:
                f.write(css_content)

            # 重新应用主题以更新预览
            await self.core.apply_theme(preview_theme_path, is_preview=True)
            return {"status": "success", "message": "预览已更新"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def stop_preview(self) -> None:
        """停止预览"""
        if self.preview_active and self.current_theme:
            try:
                preview_theme_path = self.preview_path / self.current_theme.name
                await self.core.remove_theme(preview_theme_path)
            except Exception:
                pass  # 忽略清理错误

            self.preview_active = False
            self.current_theme = None

        # 清理临时目录
        try:
            shutil.rmtree(self.preview_path)
        except Exception:
            pass

    async def handle_websocket(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """处理WebSocket连接"""
        self.websocket = websocket
        try:
            async for message in websocket:
                if isinstance(message, str):
                    # 处理CSS更新
                    result = await self.update_preview(message)
                    await websocket.send(json.dumps(result))
                elif isinstance(message, bytes):
                    # 处理二进制数据（如果需要）
                    pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.websocket = None
            await self.stop_preview()

    def __del__(self):
        """清理资源"""
        try:
            if self.preview_path.exists():
                shutil.rmtree(self.preview_path)
        except Exception:
            pass 