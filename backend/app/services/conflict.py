from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking import LabBookingSlot, LabBookingRequest

async def check_conflict(lab_id: int, week: int, day: int, start: int, end: int, db: AsyncSession) -> bool:
    q = select(LabBookingSlot).join(LabBookingRequest).where(
        LabBookingSlot.lab_id == lab_id,
        LabBookingSlot.week_number == week,
        LabBookingSlot.day_of_week == day,
        LabBookingSlot.period_start < end,
        LabBookingSlot.period_end > start,
        LabBookingRequest.status.in_(["approved", "pending"])
    )
    result = await db.execute(q)
    return result.first() is not None
