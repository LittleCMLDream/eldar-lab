"""Pydantic schemas for booking request/response models."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookingSlotCreate(BaseModel):
    lab_id: int
    week_number: int
    day_of_week: int
    period_start: int
    period_end: int


class BookingCreate(BaseModel):
    semester_id: int
    reason: str
    course_name: str
    class_names: str
    slots: list[BookingSlotCreate]


class BookingRead(BaseModel):
    id: int
    request_no: str
    status: str
    reason: str
    course_name: str

    class Config:
        from_attributes = True


class BookingApprovalResponse(BaseModel):
    id: int
    request_no: str
    status: str
    approved_at: Optional[datetime] = None
    message: str

    class Config:
        from_attributes = True
