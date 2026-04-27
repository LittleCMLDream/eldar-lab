import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def send_notification(db: AsyncSession, user_id: int, msg_type: str, payload: dict):
    data = {"user_id": user_id, "type": msg_type, **payload}
    safe_payload = json.dumps(data).replace("'", "''")
    await db.execute(text(f"SELECT pg_notify('booking_update', '{safe_payload}')"))
