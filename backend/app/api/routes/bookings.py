"""Booking API routes including creation, listing, and approval."""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.core.database import get_db
from app.models.booking import LabBookingRequest, LabBookingSlot
from app.schemas.booking import BookingCreate, BookingRead, BookingApprovalResponse

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingRead])
async def list_bookings(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(LabBookingRequest))
    return res.scalars().all()


@router.post("/", status_code=201)
async def create_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db)):
    new_req = LabBookingRequest(
        semester_id=booking.semester_id,
        request_no="REQ-" + str(hash(booking.course_name))[:8],
        teacher_id=1,  # Hardcoded for now
        reason=booking.reason,
        course_name=booking.course_name,
        class_names=booking.class_names,
    )
    db.add(new_req)
    await db.flush()
    for s in booking.slots:
        db.add(
            LabBookingSlot(
                request_id=new_req.id,
                lab_id=s.lab_id,
                week_number=s.week_number,
                day_of_week=s.day_of_week,
                period_start=s.period_start,
                period_end=s.period_end,
            )
        )
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        if "no_overlapping_lab_slots" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Booking conflict: one or more time slots overlap with an existing approved booking.",
            )
        raise
    return {"status": "pending"}


@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    req = await db.get(LabBookingRequest, booking_id)
    if not req:
        raise HTTPException(status_code=404, detail="Booking not found")
    return req


@router.put("/{booking_id}/approve", response_model=BookingApprovalResponse)
async def approve_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Approve a booking request, update status, and notify the teacher via PG NOTIFY."""
    req = await db.get(LabBookingRequest, booking_id)
    if not req:
        raise HTTPException(status_code=404, detail="Booking not found")

    if req.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot approve booking with status '{req.status}'. Only 'pending' bookings can be approved.",
        )

    req.status = "approved"
    req.approved_at = datetime.now(timezone.utc)
    req.approver_id = 1  # Hardcoded admin for now
    await db.commit()

    # Send PG NOTIFY to the teacher about the approval
    teacher_id = req.teacher_id
    if teacher_id:
        payload = json.dumps(
            {
                "booking_id": req.id,
                "request_no": req.request_no,
                "status": "approved",
                "user_id": teacher_id,
                "message": f"Your booking {req.request_no} has been approved.",
            }
        )
        await db.execute(f"SELECT pg_notify('booking_update', '{payload}')")

    return BookingApprovalResponse(
        id=req.id,
        request_no=req.request_no,
        status=req.status,
        approved_at=req.approved_at,
        message="Booking approved successfully.",
    )


@router.put("/{booking_id}/reject")
async def reject_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    """Reject a booking request and notify the teacher."""
    req = await db.get(LabBookingRequest, booking_id)
    if not req:
        raise HTTPException(status_code=404, detail="Booking not found")

    if req.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reject booking with status '{req.status}'. Only 'pending' bookings can be rejected.",
        )

    req.status = "rejected"
    req.approved_at = datetime.now(timezone.utc)
    req.approver_id = 1
    await db.commit()

    teacher_id = req.teacher_id
    if teacher_id:
        payload = json.dumps(
            {
                "booking_id": req.id,
                "request_no": req.request_no,
                "status": "rejected",
                "user_id": teacher_id,
                "message": f"Your booking {req.request_no} has been rejected.",
            }
        )
        await db.execute(f"SELECT pg_notify('booking_update', '{payload}')")

    return {"id": req.id, "request_no": req.request_no, "status": "rejected"}
