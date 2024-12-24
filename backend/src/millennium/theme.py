import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from ..config import get_settings

settings = get_settings()

class ThemeManager:
    def __init__(self):
        self.templates_dir = settings.THEMES_PATH / "templates"
        self.output_dir = settings.THEMES_PATH / "output"
        self._ensure_directories()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def create_theme(self, name: str, config: Dict) -> Path:
        """创建新主题"""
        theme_dir = self.output_dir / name
        if theme_dir.exists():
            raise ValueError(f"主题 '{name}' 已存在")

        # 创建主题目录
        theme_dir.mkdir(parents=True)

        # 创建主题配置文件
        config_path = theme_dir / "skin.json"
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # 创建基本文件
        self._create_base_files(theme_dir)

        return theme_dir

    def _create_base_files(self, theme_dir: Path):
        """创建主题的基本文件"""
        files = {
            "webkit.css": "/* 全局样式 */\n",
            "libraryroot.custom.css": "/* 库页面样式 */\n",
            "friends.custom.css": "/* 好友列表样式 */\n",
            "bigpicture.custom.css": "/* 大屏幕模式样式 */\n",
        }

        for filename, content in files.items():
            file_path = theme_dir / filename
            file_path.write_text(content, encoding="utf-8")

    async def get_theme(self, name: str) -> Optional[Dict]:
        """获取主题信息"""
        theme_dir = self.output_dir / name
        if not theme_dir.exists():
            return None

        config_path = theme_dir / "skin.json"
        if not config_path.exists():
            return None

        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    async def list_themes(self) -> List[Dict]:
        """列出所有主题"""
        themes = []
        for theme_dir in self.output_dir.iterdir():
            if not theme_dir.is_dir():
                continue

            config_path = theme_dir / "skin.json"
            if not config_path.exists():
                continue

            with config_path.open("r", encoding="utf-8") as f:
                config = json.load(f)
                config["path"] = str(theme_dir)
                themes.append(config)

        return themes

    async def update_theme(self, name: str, updates: Dict) -> bool:
        """更新主题"""
        theme_dir = self.output_dir / name
        if not theme_dir.exists():
            return False

        config_path = theme_dir / "skin.json"
        if not config_path.exists():
            return False

        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)

        config.update(updates)

        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        return True

    async def delete_theme(self, name: str) -> bool:
        """删除主题"""
        theme_dir = self.output_dir / name
        if not theme_dir.exists():
            return False

        shutil.rmtree(theme_dir)
        return True

    async def export_theme(self, name: str, target_dir: Path) -> Optional[Path]:
        """导出主题"""
        theme_dir = self.output_dir / name
        if not theme_dir.exists():
            return None

        target_path = target_dir / f"{name}.zip"
        shutil.make_archive(str(target_path.with_suffix("")), "zip", theme_dir)

        return target_path

    async def import_theme(self, zip_path: Path) -> Optional[str]:
        """导入主题"""
        import tempfile
        import zipfile

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 解压主题文件
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_path)

            # 查找skin.json
            config_files = list(temp_path.rglob("skin.json"))
            if not config_files:
                return None

            config_path = config_files[0]
            theme_dir = config_path.parent

            # 读取主题配置
            with config_path.open("r", encoding="utf-8") as f:
                config = json.load(f)

            # 移动到输出目录
            theme_name = config.get("name", zip_path.stem)
            target_dir = self.output_dir / theme_name

            if target_dir.exists():
                shutil.rmtree(target_dir)

            shutil.copytree(theme_dir, target_dir)
            return theme_name 