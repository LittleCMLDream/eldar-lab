from sqlalchemy import Column, String, Integer, SmallInteger
from app.models.base import Base, TimestampMixin
class LabRoom(TimestampMixin, Base):
    __tablename__ = "lab_rooms"
    name = Column(String(50), nullable=False)
    building = Column(String(20), nullable=False, index=True)
    room_number = Column(String(20), nullable=False)
    pc_count = Column(Integer)
    capacity = Column(Integer)
    status = Column(SmallInteger, default=1)