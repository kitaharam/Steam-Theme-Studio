from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config import get_settings
from src.database import init_db
from src.routes import api_router
from src.websocket import websocket_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时运行
    await init_db()
    yield
    # 关闭时运行
    pass

app = FastAPI(
    title="Steam Theme Studio API",
    description="Steam主题设计器的后端API服务",
    version="0.1.0",
    lifespan=lifespan,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router)
app.include_router(websocket_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG,
    ) 