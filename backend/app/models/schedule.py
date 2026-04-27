from sqlalchemy import Column, String, Integer, SmallInteger, BigInteger
from app.models.base import Base, TimestampMixin

class LabSchedule(TimestampMixin, Base):
    __tablename__ = "lab_schedules"
    semester_id = Column(BigInteger, nullable=False, index=True)
    course_name = Column(String(100), nullable=False)
    teacher_id = Column(BigInteger, index=True)
    class_names = Column(String(500))
    week_start = Column(Integer)
    week_end = Column(Integer)
    week_type = Column(String(10))
    day_of_week = Column(SmallInteger)
    period_start = Column(SmallInteger)
    period_end = Column(SmallInteger)
