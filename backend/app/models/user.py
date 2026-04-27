from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base, TimestampMixin
class Role(str, enum.Enum):
    TEACHER = "teacher"
    ADMIN = "admin"
class User(TimestampMixin, Base):
    __tablename__ = "users"
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.TEACHER)
    bookings = relationship("LabBookingRequest", back_populates="teacher")