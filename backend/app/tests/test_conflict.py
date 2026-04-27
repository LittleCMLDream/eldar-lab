"""Tests for conflict detection logic."""
import pytest
from app.services.conflict import check_conflict
from app.models.booking import LabBookingRequest, LabBookingSlot
from app.models.user import User, Role

@pytest.mark.asyncio
async def test_no_conflict_when_empty(db_session):
    """Should return False when no bookings exist."""
    # Create dummy user first
    db_session.add(User(username="test", hashed_password="hash", role=Role.TEACHER))
    await db_session.flush()
    user = (await db_session.execute(
        __import__('sqlalchemy').select(User)
    )).scalars().first()
    
    # Create a booking request
    req = LabBookingRequest(semester_id=1, request_no="TEST-1", teacher_id=user.id, status="approved")
    db_session.add(req)
    await db_session.flush()
    
    result = await check_conflict(1, 5, 1, 3, 4, db_session)
    assert result is False

@pytest.mark.asyncio
async def test_conflict_detected(db_session):
    """Should return True when overlapping slot exists."""
    db_session.add(User(username="test", hashed_password="hash", role=Role.TEACHER))
    await db_session.flush()
    user = (await db_session.execute(
        __import__('sqlalchemy').select(User)
    )).scalars().first()

    req = LabBookingRequest(semester_id=1, request_no="TEST-1", teacher_id=user.id, status="approved")
    db_session.add(req)
    await db_session.flush()
    
    # Add overlapping slot: lab 1, week 5, day 1, periods 3-4
    slot = LabBookingSlot(
        request_id=req.id, lab_id=1, week_number=5, day_of_week=1,
        period_start=3, period_end=4
    )
    db_session.add(slot)
    await db_session.commit()
    
    # Check conflict for periods 4-5 (overlaps with 3-4)
    result = await check_conflict(1, 5, 1, 4, 5, db_session)
    assert result is True

@pytest.mark.asyncio
async def test_no_conflict_different_lab(db_session):
    """Should not conflict if lab is different."""
    db_session.add(User(username="test", hashed_password="hash", role=Role.TEACHER))
    await db_session.flush()
    user = (await db_session.execute(
        __import__('sqlalchemy').select(User)
    )).scalars().first()
    
    req = LabBookingRequest(semester_id=1, request_no="TEST-1", teacher_id=user.id, status="approved")
    db_session.add(req)
    await db_session.flush()
    
    db_session.add(LabBookingSlot(request_id=req.id, lab_id=1, week_number=5, day_of_week=1, period_start=3, period_end=4))
    await db_session.commit()
    
    # Check lab 2, same time -> no conflict
    result = await check_conflict(2, 5, 1, 3, 4, db_session)
    assert result is False
