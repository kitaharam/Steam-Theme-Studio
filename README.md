# Steam主题设计器 (Steam Theme Studio)

一个用于创建、预览和管理Steam客户端主题的可视化工具。本项目基于 [Millennium](https://github.com/SteamClientHomebrew/Millennium) 框架，提供了友好的图形界面来设计和开发Steam主题。

## 使用方式

### 方式一：独立应用（推荐）
1. 从 [Releases](https://github.com/your-repo/releases) 页面下载最新版本
2. 根据您的操作系统选择对应的安装包：
   - Windows: `SteamThemeStudio-Setup.exe`
   - macOS: `SteamThemeStudio.dmg`
   - Linux: `steam-theme-studio.AppImage`
3. 运行安装程序，按照提示完成安装
4. 启动应用即可开始使用

### 方式二：Web应用
访问：[https://your-domain.com](https://your-domain.com)

### 方式三：本地开发

#### 环境要求
- Node.js 18+
- Python 3.11+
- pnpm
- Poetry

#### 前端依赖
```json
{
  "dependencies": {
    "@heroicons/react": "^2.0.0",
    "clsx": "^2.1.1",
    "monaco-editor": "^0.52.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.0.0",
    "sonner": "^1.7.1",
    "tailwind-merge": "^2.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.0.0",
    "postcss": "^8.0.0",
    "tailwindcss": "^3.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

#### 后端依赖
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.105.0"
uvicorn = "^0.24.0"
python-multipart = "^0.0.6"
websockets = "^12.0"
sqlalchemy = "^2.0.23"
aiosqlite = "^0.19.0"
pydantic = "^2.5.2"
pydantic-settings = "^2.1.0"
watchfiles = "^0.21.0"

[tool.poetry.group.dev.dependencies]
black = "^23.12.0"
isort = "^5.13.2"
pytest = "^7.4.3"
pytest-asyncio = "^0.23.2"
httpx = "^0.25.2"
```

#### 安装步骤
1. 克隆项目
```bash
git clone [项目地址]
cd steampack
```

2. 安装前端依赖
```bash
cd frontend
pnpm install
```

3. 安装后端依赖
```bash
cd ../backend
poetry install
```

4. 启动开发服务器
```bash
# 前端开发服务器
cd frontend
pnpm dev

# 后端开发服务器
cd backend
poetry run python -m src.main
```

## 项目配置文件

### 前端配置
1. `vite.config.ts` - Vite配置
2. `tailwind.config.js` - TailwindCSS配置
3. `tsconfig.json` - TypeScript配置
4. `.env` - 环境变量

### 后端配置
1. `pyproject.toml` - Python项目配置
2. `.env` - 环境变量
3. `alembic.ini` - 数据库迁移配置

## 当前开发状态

### 已完成功能
- 基础项目架构搭建
- 基础UI组件开发
- 路由系统实现
- WebSocket通信基础架构
- Node.js环境配置
- 前端依赖安装
- Python后端环境配置

### 待解决问题
1. 环境配置问题
   - [x] Python依赖安装
   - [ ] 验证开发环境的完整性
2. 核心功能缺失
   - 主题预览组件
   - 主题编辑器组件
   - Millennium框架集成验证

## 优先级分析

### P0（必须立即解决）
1. 环境配置问题
   - 完成Python后端依赖安装（特别是greenlet）
   - 验证开发环境的完整性

2. 核心功能实现
   - 实现主题预览组件（ThemePreview）
   - 实现主题编辑器组件（ThemeEditor）
   - 完成与Millennium框架的基础交互

### P1（高优先级）
1. 主题管理基础功能
   - 主题文件的读写操作
   - 主题配置文件处理
   - 基础预览功能

2. 实时预览系统
   - WebSocket实时更新机制
   - 预览窗口实现
   - 主题切换功能

### P2（中优先级）
1. 用户体验优化
   - 错误处理和提示
   - 加载状态管理
   - 基础测试用例编写

## 短期开发计划（2周内）

### 第一周
1. 环境配置（1-2天）
   - [x] 验证Node.js环境配置
   - [x] 完成Python依赖安装
   - [x] 确保前端开发依赖正确安装
   - [ ] 验证开发环境完整性

2. 核心组件开发（3-4天）
   - [ ] 实现ThemePreview组件
   - [ ] 实现ThemeEditor组件
   - [ ] 完成基础主题编辑功能

3. Millennium集成（1-2天）
   - [ ] 验证Millennium框架集成
   - [ ] 实现基础主题加载功能
   - [ ] 测试主题文件处理

### 第二周
1. 实时预览功能（2-3天）
   - [ ] 完善WebSocket通信
   - [ ] 实现实时预览更新
   - [ ] 添加预览控制功能

2. 主题管理功能（2-3天）
   - [ ] 实现主题文件管理
   - [ ] 添加主题配置界面
   - [ ] 完成基础主题操作功能

3. 测试和修复（2天）
   - [ ] 编写基础测试用例
   - [ ] 修复已知问题
   - [ ] 优化用户体验

## 开发计划

### 第一阶段：基础架构（预计2周）
- [x] 项目初始化
  - [x] 前端项目搭建（React + TypeScript）
  - [x] 后端项目搭建（Python）
  - [x] 开发环境配置
  - [x] 基础依赖安装

- [ ] 核心功能框架
  - [x] Millennium框架集成
  - [x] 主题文件系统设计
  - [x] WebSocket通信实现
  - [x] 基础UI框架搭建
  - [ ] 验证开发环境完整性

### 第二阶段：编辑器开发（预计3周）
- [ ] CSS编辑器实现
  - [ ] Monaco Editor集成
  - [ ] 语法高亮和自动完成
  - [ ] 实时保存功能
  - [ ] 主题文件管理

- [ ] 预览系统
  - [ ] 实时预览窗口
  - [ ] 预览刷新机制
  - [ ] 多页面预览支持
  - [ ] 响应式预览

### 第三阶段：主题管理（预计2周）
- [ ] 主题配置系统
  - [ ] 变量管理器
  - [ ] 颜色系统
  - [ ] 组件库
  - [ ] 预设管理

- [ ] 资源管理
  - [ ] 图片资源管理
  - [ ] 字体管理
  - [ ] 资源导入导出

### 第四阶段：工具优化（预计2周）
- [ ] 用户体验优化
  - [ ] 快捷键支持
  - [ ] 操作历史记录
  - [ ] 错误提示优化
  - [ ] 性能优化

- [ ] 发布系统
  - [ ] 主题打包
  - [ ] 主题验证
  - [ ] 发布工具

## 技术栈

### 前端
- React 18
- TypeScript 5
- Monaco Editor
- Electron（可选，用于桌面应用）
- TailwindCSS
- Vite

### 后端
- Python 3.11+
- FastAPI
- WebSocket
- SQLite（用于本地数据存储）

### 开发工具
- Git
- Node.js 18+
- pnpm（包管理器）
- Poetry（Python依赖管理）

## 项目结构
```
steampack/
├── README.md                 # 项目文档
├── frontend/                 # 前端代码
│   ├── src/                 # React + TypeScript源代码
│   ├── public/              # 静态资源
│   └── package.json         # 前端依赖配置
│
├── backend/                 # 后端代码
│   ├── src/                # Python源代码
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python依赖配置
│
├── themes/                 # 主题相关
│   ├── templates/         # 主题模板
│   └── output/           # 生成的主题包
│
└── docs/                  # 项目文档
    ├── development/      # 开发指南
    └── user-guide/      # 用户使用手册
```

## 开发规范

### Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式（不影响代码运行的变动）
- refactor: 重构
- test: 增加测试
- chore: 构建过程或辅助工具的变动

### 代码规范
- 前端：使用ESLint + Prettier
- 后端：使用Black + isort
- 提交前需要通过所有Lint检查

## 如何开始开发

1. 克隆项目
```bash
git clone [项目地址]
cd steampack
```

2. 安装依赖
```bash
# 前端依赖
cd frontend
pnpm install

# 后端依赖
cd ../backend
poetry install
```

3. 启动开发服务器
```bash
# 前端开发服务器
cd frontend
pnpm dev

# 后端开发服务器
cd backend
poetry run python -m src.main
```

## 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License

## 打包说明

### 桌面应用打包
1. 安装electron-builder
```bash
pnpm add -D electron-builder
```

2. 配置package.json
```json
{
  "build": {
    "appId": "com.your-domain.steam-theme-studio",
    "productName": "Steam Theme Studio",
    "directories": {
      "output": "dist"
    },
    "win": {
      "target": ["nsis"]
    },
    "mac": {
      "target": ["dmg"]
    },
    "linux": {
      "target": ["AppImage"]
    }
  }
}
```

3. 执行打包
```bash
pnpm build
pnpm electron-builder
```

### Web应用部署
1. 构建前端
```bash
cd frontend
pnpm build
```

2. 构建后端
```bash
cd backend
poetry build
```

3. Docker部署（可选）
```dockerfile
# Dockerfile配置说明
...
```
