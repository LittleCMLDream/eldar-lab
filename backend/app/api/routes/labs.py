"""Lab Room API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.lab import LabRoom
from pydantic import BaseModel

router = APIRouter(prefix="/api/labs", tags=["labs"])

class LabCreate(BaseModel):
    name: str; building: str; room_number: str; pc_count: int = 0; capacity: int = 0

class LabRead(BaseModel):
    id: int; name: str; building: str; room_number: str
    class Config: from_attributes = True

@router.get("/", response_model=list[LabRead])
async def list_labs(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(LabRoom).where(LabRoom.status == 1).order_by(LabRoom.building, LabRoom.room_number))
    return res.scalars().all()

@router.post("/", status_code=201, response_model=LabRead)
async def create_lab(lab: LabCreate, db: AsyncSession = Depends(get_db)):
    new_lab = LabRoom(**lab.model_dump())
    db.add(new_lab); await db.commit(); await db.refresh(new_lab)
    return new_lab

@router.delete("/{lab_id}")
async def delete_lab(lab_id: int, db: AsyncSession = Depends(get_db)):
    lab = await db.get(LabRoom, lab_id)
    if not lab: raise HTTPException(404, "Not found")
    lab.status = 0; await db.commit(); return {"status": "deleted"}

@router.post("/seed")
async def seed_labs(db: AsyncSession = Depends(get_db)):
    """Seed initial lab room data (10 rooms from actual data)."""
    rooms = [
        {"name": "机器学习实验室", "building": "逸夫楼", "room_number": "602", "pc_count": 60, "capacity": 60},
        {"name": "移动应用开发实验室", "building": "逸夫楼", "room_number": "605", "pc_count": 60, "capacity": 58},
        {"name": "人工智能学院室", "building": "逸夫楼", "room_number": "702", "pc_count": 58, "capacity": 56},
        {"name": "软件工程实训室", "building": "逸夫楼", "room_number": "607", "pc_count": 56, "capacity": 50},
        {"name": "程序设计实验室", "building": "逸夫楼", "room_number": "604", "pc_count": 56, "capacity": 50},
        {"name": "微机原理实验室", "building": "文综楼", "room_number": "1402", "pc_count": 58, "capacity": 53},
        {"name": "智能机器人实验室", "building": "文综楼", "room_number": "1406", "pc_count": 60, "capacity": 58},
        {"name": "博达楼实验室1", "building": "博达楼", "room_number": "210", "pc_count": 60, "capacity": 58},
        {"name": "博达楼实验室2", "building": "博达楼", "room_number": "208", "pc_count": 60, "capacity": 58},
        {"name": "博达楼实验室3", "building": "博达楼", "room_number": "110", "pc_count": 55, "capacity": 55},
    ]
    from app.models.lab import LabRoom
    existing = await db.execute(select(LabRoom))
    if existing.scalars().first():
        return {"status": "already seeded", "count": len(rooms)}
    for r in rooms:
        db.add(LabRoom(**r))
    await db.commit()
    return {"status": "seeded", "count": len(rooms)}
