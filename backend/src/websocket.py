from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, client_id: str):
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@websocket_router.websocket("/ws/test")
async def websocket_test(websocket: WebSocket):
    await manager.connect(websocket, "test")
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    response = {
                        "type": "pong",
                        "time": datetime.now().isoformat(),
                        "message": "服务器正常运行"
                    }
                    await manager.send_message(json.dumps(response), websocket)
            except json.JSONDecodeError:
                await manager.send_message(json.dumps({"error": "无效的JSON格式"}), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "test")
    except Exception as e:
        print(f"WebSocket错误: {str(e)}")
        manager.disconnect(websocket, "test") 