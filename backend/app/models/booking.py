from sqlalchemy import Column, String, Integer, SmallInteger, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
class LabBookingRequest(TimestampMixin, Base):
    __tablename__ = "lab_booking_requests"
    semester_id = Column(BigInteger, nullable=False)
    request_no = Column(String(32), unique=True, nullable=False)
    teacher_id = Column(BigInteger, ForeignKey("users.id"))
    reason = Column(String(20))
    course_name = Column(String(100))
    class_names = Column(String(500))
    student_count = Column(Integer)
    content = Column(Text)
    status = Column(String(20), default="pending")
    approver_id = Column(BigInteger)
    approved_at = Column(DateTime)
    teacher = relationship("User", back_populates="bookings")
    slots = relationship("LabBookingSlot", back_populates="request", cascade="all, delete-orphan")
class LabBookingSlot(TimestampMixin, Base):
    __tablename__ = "lab_booking_slots"
    lab_id = Column(BigInteger, nullable=False, index=True)
    week_number = Column(SmallInteger, nullable=False)
    day_of_week = Column(SmallInteger, nullable=False)
    period_start = Column(SmallInteger, nullable=False)
    period_end = Column(SmallInteger, nullable=False)
    request_id = Column(BigInteger, ForeignKey("lab_booking_requests.id"), nullable=False)
    request = relationship("LabBookingRequest", back_populates="slots")