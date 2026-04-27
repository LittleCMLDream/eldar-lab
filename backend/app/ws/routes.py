import asyncio, json, asyncpg
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.config import settings
from app.ws.manager import manager

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def ws_endpoint(ws: WebSocket, user_id: int):
    await manager.connect(ws, user_id)
    dsn = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(dsn)
    await conn.add_listener("booking_update", _on_notify)
    try:
        while True:
            await asyncio.sleep(1)
            if ws.client_state.value != 1: break
    except WebSocketDisconnect: pass
    finally:
        manager.disconnect(ws, user_id)
        await conn.remove_listener("booking_update", _on_notify)
        await conn.close()

async def _on_notify(conn, pid, channel, payload):
    try:
        data = json.loads(payload)
        if data.get("user_id") is not None:
            await manager.send_to(payload, int(data["user_id"]))
    except: pass
