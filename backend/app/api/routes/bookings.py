from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.booking import BookingCreate, BookingRead
from app.models.booking import LabBookingRequest, LabBookingSlot
from sqlalchemy import select
router = APIRouter(prefix="/api/bookings", tags=["bookings"])
@router.get("/", response_model=list[BookingRead])
async def list_bookings(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(LabBookingRequest))
    return res.scalars().all()
@router.post("/", status_code=201)
async def create_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db)):
    # Conflict Check Logic Here
    # ...
    new_req = LabBookingRequest(
        semester_id=booking.semester_id,
        request_no="REQ-" + str(hash(booking.course_name))[:8],
        teacher_id=1, # Hardcoded for now
        reason=booking.reason,
        course_name=booking.course_name,
        class_names=booking.class_names
    )
    db.add(new_req)
    await db.flush()
    for s in booking.slots:
        db.add(LabBookingSlot(
            request_id=new_req.id, lab_id=s.lab_id,
            week_number=s.week_number, day_of_week=s.day_of_week,
            period_start=s.period_start, period_end=s.period_end
        ))
    await db.commit()
    return {"status": "pending"}