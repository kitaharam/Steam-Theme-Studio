"""
简单的VDF（Valve Data Format）解析器
用于读取和修改Steam配置文件
"""

import re
from typing import Dict, Any, Optional

class VDFParser:
    def __init__(self):
        self.indent = "  "
        self.current_indent = 0

    def parse(self, content: str) -> dict:
        """解析VDF格式的内容为字典"""
        lines = content.strip().split("\n")
        result = {}
        stack = [(result, 0)]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 计算当前行的缩进级别
            indent_level = (len(line) - len(line.lstrip())) // 2
            line = line.strip()

            # 处理键值对
            if line.startswith('"') and line.endswith('"'):
                # 单行键值对
                key = line.strip('"')
                current_dict = stack[-1][0]
                current_dict[key] = {}
            elif line.startswith('"'):
                # 键值对开始
                key = line.strip('"')
                value = {}
                current_dict = stack[-1][0]
                current_dict[key] = value
                stack.append((value, indent_level))
            elif line == "{":
                continue
            elif line == "}":
                if stack:
                    stack.pop()

        return result

    def format(self, data: dict, indent_level: int = 0) -> str:
        """将字典格式化为VDF格式的字符串"""
        result = []
        indent = self.indent * indent_level

        for key, value in data.items():
            if isinstance(value, dict):
                result.append(f'{indent}"{key}"')
                result.append(f"{indent}{{")
                result.append(self.format(value, indent_level + 1))
                result.append(f"{indent}}}")
            else:
                result.append(f'{indent}"{key}" "{value}"')

        return "\n".join(result)

    def update_theme_config(self, content: str, theme_name: str) -> str:
        """更新VDF配置中的主题设置"""
        try:
            data = self.parse(content)
            
            # 确保基本结构存在
            if "libraryconfig" not in data:
                data["libraryconfig"] = {}
            if "settings" not in data["libraryconfig"]:
                data["libraryconfig"]["settings"] = {}
            
            # 更新主题设置
            data["libraryconfig"]["settings"]["SteamTheme"] = theme_name
            
            # 格式化回VDF格式
            return self.format(data)
            
        except Exception as e:
            raise ValueError(f"更新VDF配置失败: {str(e)}")

    def get_current_theme(self, content: str) -> str:
        """获取当前主题名称"""
        try:
            data = self.parse(content)
            return data.get("libraryconfig", {}).get("settings", {}).get("SteamTheme", "")
        except Exception:
            return ""