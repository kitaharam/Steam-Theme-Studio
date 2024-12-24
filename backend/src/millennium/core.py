import asyncio
import sys
import shutil
import json
from pathlib import Path
from typing import Optional, Dict, List, Any
from ..config import get_settings
from .vdf_parser import VDFParser

settings = get_settings()

class MillenniumCore:
    def __init__(self):
        self.millennium_path = settings.MILLENNIUM_PATH
        self.steam_path = self._get_steam_path()
        self.initialized = False
        self.steam_ui_path = self.steam_path / "steamui" if self.steam_path else None
        self.skins_path = self.steam_ui_path / "skins" if self.steam_ui_path else None
        self.themes_path = settings.THEMES_PATH
        self.vdf_parser = VDFParser()

    def _get_steam_path(self) -> Optional[Path]:
        """获取Steam安装路径"""
        if sys.platform == "win32":
            import winreg
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam") as key:
                    return Path(winreg.QueryValueEx(key, "InstallPath")[0])
            except WindowsError:
                return None
        elif sys.platform == "darwin":
            paths = [
                Path.home() / "Library/Application Support/Steam",
            ]
            for path in paths:
                if path.exists():
                    return path
        else:  # Linux
            paths = [
                Path.home() / ".local/share/Steam",
                Path.home() / ".steam/steam",
            ]
            for path in paths:
                if path.exists():
                    return path
        return None

    async def initialize(self):
        """初始化Millennium框架"""
        if self.initialized:
            return

        if not self.millennium_path.exists():
            raise RuntimeError(f"Millennium框架未找到: {self.millennium_path}")

        if not self.steam_path:
            raise RuntimeError("未找到Steam安装路径")

        if not self.steam_ui_path or not self.steam_ui_path.exists():
            raise RuntimeError("Steam UI目录未找到")

        # 创建主题目录
        self.skins_path.mkdir(exist_ok=True)

        # 初始化其他必要的设置
        await self._setup_environment()
        self.initialized = True

    async def _setup_environment(self):
        """设置运行环境"""
        # 确保CEF调试功能已启用
        cef_debug_file = self.steam_path / ".cef-enable-remote-debugging"
        if not cef_debug_file.exists():
            cef_debug_file.touch()

        # 确保配置目录存在
        config_dir = self.steam_path / "config"
        config_dir.mkdir(exist_ok=True)

        # 确保libraryconfig.vdf存在
        library_config = config_dir / "libraryconfig.vdf"
        if not library_config.exists():
            library_config.write_text('{\n  "libraryconfig"\n  {\n    "settings"\n    {\n    }\n  }\n}\n')

    async def validate_theme(self, theme_path: Path) -> bool:
        """验证主题是否有效"""
        if not theme_path.exists():
            return False

        # 检查必需文件
        required_files = ["skin.json", "webkit.css"]
        if not all((theme_path / file).exists() for file in required_files):
            return False

        # 验证skin.json格式
        try:
            config = self.get_theme_config(theme_path)
            required_fields = ["name", "author", "version"]
            return all(field in config for field in required_fields)
        except (json.JSONDecodeError, FileNotFoundError):
            return False

    def get_theme_config(self, theme_path: Path) -> Dict:
        """获取主题配置"""
        config_path = theme_path / "skin.json"
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    async def apply_theme(self, theme_path: Path, is_preview: bool = False) -> None:
        """应用主题"""
        if not await self.validate_theme(theme_path):
            raise ValueError("无效的主题")

        theme_config = self.get_theme_config(theme_path)
        theme_name = theme_config["name"]
        target_path = self.skins_path / theme_name

        # 如果目标目录已存在，先删除
        if target_path.exists():
            shutil.rmtree(target_path)

        # 复制主题文件到Steam主题目录
        shutil.copytree(theme_path, target_path)

        # 更新Steam配置文件
        if not is_preview:
            await self._update_steam_config(theme_name)

    async def _update_steam_config(self, theme_name: str):
        """更新Steam配置文件"""
        config_path = self.steam_path / "config/libraryconfig.vdf"
        
        try:
            # 读取现有配置
            content = config_path.read_text(encoding="utf-8")
            
            # 更新配置
            new_content = self.vdf_parser.update_theme_config(content, theme_name)
            
            # 备份原配置
            backup_path = config_path.with_suffix(".vdf.bak")
            shutil.copy2(config_path, backup_path)
            
            # 写入新配置
            config_path.write_text(new_content, encoding="utf-8")
            
        except Exception as e:
            raise RuntimeError(f"更新Steam配置失败: {str(e)}")

    async def remove_theme(self, theme_path: Path):
        """移除主题"""
        if not theme_path.exists():
            return

        theme_config = self.get_theme_config(theme_path)
        theme_name = theme_config["name"]
        target_path = self.skins_path / theme_name

        if target_path.exists():
            shutil.rmtree(target_path)

    async def restart_steam(self):
        """重启Steam客户端"""
        if sys.platform == "win32":
            await asyncio.create_subprocess_shell("taskkill /F /IM steam.exe")
            await asyncio.sleep(1)
            await asyncio.create_subprocess_shell(str(self.steam_path / "steam.exe"))
        else:
            await asyncio.create_subprocess_shell("pkill steam")
            await asyncio.sleep(1)
            await asyncio.create_subprocess_shell("steam") 

    async def list_themes(self) -> List[Dict[str, Any]]:
        """获取所有主题列表"""
        themes = []
        if not self.themes_path.exists():
            return themes

        for theme_dir in self.themes_path.iterdir():
            if theme_dir.is_dir():
                try:
                    config = self.get_theme_config(theme_dir)
                    themes.append({
                        "name": theme_dir.name,
                        "config": config,
                        "path": str(theme_dir)
                    })
                except Exception:
                    continue  # 跳过无效的主题
        return themes

    async def create_theme(self, name: str, config: Dict[str, Any]) -> Path:
        """创建新主题"""
        theme_path = self.themes_path / name
        if theme_path.exists():
            raise ValueError(f"主题 '{name}' 已存在")

        theme_path.mkdir(parents=True)
        
        # 创建主题配置文件
        config_path = theme_path / "skin.json"
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # 创建基本CSS文件
        css_path = theme_path / "webkit.css"
        css_path.write_text("/* Steam主题样式 */\n")

        return theme_path

    async def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """获取主题信息"""
        theme_path = self.themes_path / theme_name
        if not theme_path.exists():
            raise ValueError(f"主题 '{theme_name}' 不存在")

        config = self.get_theme_config(theme_path)
        return {
            "name": theme_name,
            "config": config,
            "path": str(theme_path)
        }

    async def update_theme(self, theme_name: str, config: Dict[str, Any]) -> None:
        """更新主题配置"""
        theme_path = self.themes_path / theme_name
        if not theme_path.exists():
            raise ValueError(f"主题 '{theme_name}' 不存在")

        config_path = theme_path / "skin.json"
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    async def delete_theme(self, theme_name: str) -> None:
        """删除主题"""
        theme_path = self.themes_path / theme_name
        if not theme_path.exists():
            raise ValueError(f"主题 '{theme_name}' 不存在")

        # 如果主题正在使用中，先移除它
        if self.skins_path:
            applied_path = self.skins_path / theme_name
            if applied_path.exists():
                await self.remove_theme(theme_path)

        # 删除主题目录
        shutil.rmtree(theme_path)
  