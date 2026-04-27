from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase): pass
class TimestampMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)