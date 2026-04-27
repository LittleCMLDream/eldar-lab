from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    async def connect(self, ws: WebSocket, uid: int):
        await ws.accept()
        self.active_connections.setdefault(uid, set()).add(ws)
    def disconnect(self, ws: WebSocket, uid: int):
        self.active_connections.get(uid, set()).discard(ws)
    async def send_to(self, msg: str, uid: int):
        for ws in list(self.active_connections.get(uid, [])):
            try: await ws.send_text(msg)
            except: self.active_connections.get(uid, set()).discard(ws)

manager = ConnectionManager()
