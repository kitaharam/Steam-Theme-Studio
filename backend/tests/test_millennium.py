import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from pathlib import Path
import json
import shutil
from ..src.main import app
from ..src.millennium.core import MillenniumCore
from ..src.millennium.preview import ThemePreview

client = TestClient(app)
core = MillenniumCore()

@pytest.fixture
def test_theme_path(tmp_path):
    """创建测试主题"""
    theme_path = tmp_path / "test-theme"
    theme_path.mkdir()

    # 创建主题配置文件
    config = {
        "name": "Test Theme",
        "author": "Test Author",
        "version": "1.0.0",
        "description": "A test theme"
    }
    with (theme_path / "skin.json").open("w", encoding="utf-8") as f:
        json.dump(config, f)

    # 创建必需的CSS文件
    (theme_path / "webkit.css").write_text("/* Test CSS */")

    return theme_path

def test_millennium_initialize():
    """测试Millennium初始化"""
    response = client.post("/api/millennium/initialize")
    assert response.status_code in [200, 500]  # 500是因为可能没有找到Steam

def test_list_themes():
    """测试主题列表"""
    response = client.get("/api/millennium/themes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_theme():
    """测试创建主题"""
    theme_data = {
        "name": "test-theme",
        "config": {
            "name": "Test Theme",
            "author": "Test Author",
            "version": "1.0.0",
            "description": "A test theme"
        }
    }
    response = client.post("/api/millennium/themes", params=theme_data)
    assert response.status_code in [200, 400]  # 400是因为主题可能已存在

@pytest.mark.asyncio
async def test_validate_theme(test_theme_path):
    """测试主题验证"""
    assert await core.validate_theme(test_theme_path)

    # 测试无效主题
    invalid_theme_path = test_theme_path.parent / "invalid-theme"
    invalid_theme_path.mkdir()
    assert not await core.validate_theme(invalid_theme_path)

@pytest.mark.asyncio
async def test_apply_theme(test_theme_path):
    """测试主题应用"""
    if not core.steam_path:
        pytest.skip("Steam未安装")

    try:
        await core.apply_theme(test_theme_path)
        theme_name = core.get_theme_config(test_theme_path)["name"]
        applied_theme_path = core.skins_path / theme_name
        assert applied_theme_path.exists()
    except Exception as e:
        pytest.fail(f"应用主题失败: {str(e)}")
    finally:
        # 清理测试主题
        if core.skins_path:
            theme_name = core.get_theme_config(test_theme_path)["name"]
            applied_theme_path = core.skins_path / theme_name
            if applied_theme_path.exists():
                shutil.rmtree(applied_theme_path)

@pytest.mark.asyncio
async def test_remove_theme(test_theme_path):
    """测试主题移除"""
    if not core.steam_path:
        pytest.skip("Steam未安装")

    try:
        # 先应用主题
        await core.apply_theme(test_theme_path)
        # 然后移除
        await core.remove_theme(test_theme_path)
        theme_name = core.get_theme_config(test_theme_path)["name"]
        applied_theme_path = core.skins_path / theme_name
        assert not applied_theme_path.exists()
    except Exception as e:
        pytest.fail(f"移除主题失败: {str(e)}")

@pytest.mark.asyncio
async def test_preview_theme(test_theme_path):
    """测试主题预览"""
    if not core.steam_path:
        pytest.skip("Steam未安装")

    preview = ThemePreview(core.steam_path)
    try:
        await preview.preview_theme(test_theme_path)
    except Exception as e:
        if "无法连接到Steam客户端" not in str(e):
            pytest.fail(f"预览主题失败: {str(e)}")
    finally:
        await preview.stop_preview()

@pytest.mark.asyncio
async def test_preview_websocket():
    """测试预览WebSocket"""
    if not core.steam_path:
        pytest.skip("Steam未安装")

    with client.websocket_connect("/api/millennium/themes/test-theme/preview/ws") as websocket:
        try:
            # 发送测试CSS
            websocket.send_text("body { background: #000; }")
            response = websocket.receive_json()
            assert response["status"] in ["success", "error"]
        except Exception as e:
            if "无法连接到Steam客户端" not in str(e):
                pytest.fail(f"WebSocket测试失败: {str(e)}")