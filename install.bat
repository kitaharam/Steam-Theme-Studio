@echo off
echo 开始安装 Steam Theme Studio...

REM 检查必要的工具
echo 检查必要的工具...

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo 未找到 Node.js，请先安装 Node.js 18+
    exit /b 1
)

where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo 未找到 pnpm，正在安装...
    npm install -g pnpm
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 未找到 Python，请先安装 Python 3.11+
    exit /b 1
)

where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo 未找到 Poetry，正在安装...
    curl -sSL https://install.python-poetry.org | python -
)

REM 创建必要的目录
echo 创建必要的目录...
mkdir themes\templates 2>nul
mkdir themes\output 2>nul

REM 安装前端依赖
echo 安装前端依赖...
cd frontend
call pnpm install
cd ..

REM 安装后端依赖
echo 安装后端依赖...
cd backend
call poetry install
cd ..

REM 复制环境变量文件
echo 设置环境变量...
if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
)
if not exist backend\.env (
    copy backend\.env.example backend\.env
)

echo 安装完成！
echo 使用以下命令启动开发服务器：
echo 前端: cd frontend ^&^& pnpm dev
echo 后端: cd backend ^&^& poetry run python -m src.main

pause 