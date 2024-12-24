#!/bin/bash

# 检查必要的工具
check_requirements() {
    echo "检查必要的工具..."
    
    if ! command -v node &> /dev/null; then
        echo "未找到 Node.js，请先安装 Node.js 18+"
        exit 1
    fi
    
    if ! command -v pnpm &> /dev/null; then
        echo "未找到 pnpm，正在安装..."
        npm install -g pnpm
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "未找到 Python，请先安装 Python 3.11+"
        exit 1
    fi
    
    if ! command -v poetry &> /dev/null; then
        echo "未找到 Poetry，正在安装..."
        curl -sSL https://install.python-poetry.org | python3 -
    fi
}

# 安装前端依赖
install_frontend() {
    echo "安装前端依赖..."
    cd frontend
    pnpm install
    cd ..
}

# 安装后端依赖
install_backend() {
    echo "安装后端依赖..."
    cd backend
    poetry install
    cd ..
}

# 创建必要的目录
create_directories() {
    echo "创建必要的目录..."
    mkdir -p themes/templates
    mkdir -p themes/output
}

# 复制环境变量文件
copy_env_files() {
    echo "设置环境变量..."
    if [ ! -f frontend/.env ]; then
        cp frontend/.env.example frontend/.env
    fi
    if [ ! -f backend/.env ]; then
        cp backend/.env.example backend/.env
    fi
}

# 主函数
main() {
    echo "开始安装 Steam Theme Studio..."
    
    check_requirements
    create_directories
    install_frontend
    install_backend
    copy_env_files
    
    echo "安装完成！"
    echo "使用以下命令启动开发服务器："
    echo "前端: cd frontend && pnpm dev"
    echo "后端: cd backend && poetry run python -m src.main"
}

main 