from typing import Annotated
import logging
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import BaseModel
import os
from fastapi import (
    FastAPI, 
    WebSocket,
    WebSocketDisconnect,
    Depends,
    APIRouter, 
    )
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

"""
POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
"""

app = FastAPI()

origins= [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"])

class Item(BaseModel):
    name: str
    description: str | None
    
class Controls(BaseModel):
    x: int
    y: int

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket] = {}

    async def connect(self,client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id)

    async def send_personal_message(self, client_id: str, message: str | bytes):
        if client_id == "controller-node" and self.active_connections["rover-obc"]:
            ws: WebSocket = self.active_connections["rover-obc"]
            await ws.send_bytes(message)
        else:
            await print("No connect.")

    async def broadcast(self, message: bytes, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@lru_cache
def get_controls():
    return Controls()

@app.get("/controller-node", response_model=Controls)
async def get():
    return JSONResponse({"x": 3, "y": 4})

# @app.post("/send-message/{client_id}")
# async def send_message_to_client(client_id: str, message: str):
#     await manager.send_personal_message(message, client_id)
#     return {"status": "success", "message": "Message sent"}
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    # await websocket.accept()
    try:
        while True:
            # data = await websocket.receive_text()
         
            data: bytes = await websocket.receive_bytes()
            await manager.send_personal_message(client_id, data)
            # await manager.broadcast(client_id="rover-obc", message=data)
            # await websocket.send_text(f"You said: {data}")
            # logger.info(manager.active_connections)
            pass
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"{client_id} left.")
        # await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    uvicorn.run("web_server:app", host="192.168.1.19", port=8000, reload=True)