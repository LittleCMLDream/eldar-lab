"""Excel Import API routes."""
import os, tempfile
from fastapi import APIRouter, Depends, UploadFile, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.excel_parser import parse_excel, parse_time_slot

router = APIRouter(prefix="/api/import", tags=["import"])

@router.post("/excel")
async def import_excel(file: UploadFile, semester_id: int = Query(1), db: AsyncSession = Depends(get_db)):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "请上传 .xlsx 或 .xls 文件")
    
    # Save temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp.write(await file.read()); tmp.close()
    
    try:
        records, warnings = parse_excel(tmp.name)
        if not records:
            raise HTTPException(400, f"解析失败: {warnings}")
        
        # Process records -> create LabSchedule entries
        from app.models.schedule import LabSchedule
        created = 0
        for rec in records:
            t = rec.get("time", {})
            entry = LabSchedule(
                semester_id=semester_id,
                course_name=str(rec.get("course_name", "")),
                class_names=str(rec.get("classes", "")),
                week_start=1, week_end=20,  # Default range
                week_type="全周",
                day_of_week=t.get("day", 1),
                period_start=t.get("start", 1),
                period_end=t.get("end", 1),
            )
            db.add(entry)
            created += 1
        
        await db.commit()
        return {"status": "success", "imported": created, "warnings": warnings}
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp.name)
