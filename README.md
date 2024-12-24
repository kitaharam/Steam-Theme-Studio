# Steam Theme Studio

Steam主题设计器是一个用于创建和管理Steam客户端主题的可视化工具。它提供了直观的界面来编辑CSS样式，实时预览主题效果，并支持主题的导入导出功能。

## 功能特性

- 🎨 可视化CSS编辑器
- 👁️ 实时主题预览
- 💾 主题导入导出
- 🔄 自动保存
- 📱 响应式设计
- 🌙 深色模式支持

## 技术栈

### 前端
- React 18
- TypeScript
- Vite
- TailwindCSS
- Shadcn/ui

### 后端
- Python 3.13+
- FastAPI
- SQLAlchemy
- WebSocket

## 开发环境要求

- Node.js 18+
- Python 3.13+
- pnpm
- Poetry

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/steam-theme-studio.git
cd steam-theme-studio
```

2. 安装前端依赖
```bash
cd frontend
pnpm install
```

3. 安装后端依赖
```bash
cd backend
poetry install
```

4. 启动开发服务器

前端:
```bash
cd frontend
pnpm dev
```

后端:
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 项目结构

```
steam-theme-studio/
├── frontend/           # 前端代码
│   ├── src/           # 源代码
│   ├── public/        # 静态资源
│   └── ...
├── backend/           # 后端代码
│   ├── src/          # 源代码
│   ├── tests/        # 测试文件
│   └── ...
└── README.md
```

## 开发计划

### 第一阶段：基础架构（2周）
- [x] 项目初始化
- [x] 基础架构搭建
- [ ] 核心功能框架

### 第二阶段：编辑器开发（3周）
- [ ] CSS编辑器实现
- [ ] 预览系统实现
- [ ] 主题实时渲染

### 第三阶段：主题管理（2周）
- [ ] 主题配置系统
- [ ] 主题导入导出
- [ ] 资源管理系统

### 第四阶段：工具优化（2周）
- [ ] 用户体验优化
- [ ] 性能优化
- [ ] 发布系统

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
