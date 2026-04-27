import os
import uuid
from datetime import datetime
from typing import List, Dict, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import LabBookingRequest, LabBookingSlot
from app.models.lab import LabRoom
from app.models.user import User
from app.services.excel_parser import parse_excel
from app.services.conflict import check_conflict
from app.services.notification import send_notification


class ImportResult:
    """Holds the outcome of an Excel import operation."""

    def __init__(self):
        self.created: int = 0
        self.skipped: int = 0
        self.errors: List[str] = []
        self.warnings: List[str] = []


async def _resolve_lab(lab_name: str, db: AsyncSession) -> int | None:
    """
    Resolve a lab room name like 'A-101' to its database ID.
    Tries parsing 'building-room' format, then falls back to name search.
    """
    lab_name = str(lab_name).strip()

    # Try building-room split (e.g. "A-101")
    parts = lab_name.rsplit("-", 1)
    if len(parts) == 2:
        building, room_number = parts
        stmt = select(LabRoom).where(
            LabRoom.building == building.strip(),
            LabRoom.room_number == room_number.strip(),
        )
        result = await db.execute(stmt)
        lab = result.scalars().first()
        if lab:
            return lab.id

    # Fallback: search by name
    stmt = select(LabRoom).where(LabRoom.name == lab_name)
    result = await db.execute(stmt)
    lab = result.scalars().first()
    return lab.id if lab else None


async def _resolve_teacher(teacher_name: str, db: AsyncSession) -> int | None:
    """Resolve a teacher name to a user ID."""
    stmt = select(User).where(User.username == str(teacher_name).strip())
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user.id if user else None


async def import_schedule(
    file_path: str,
    semester_id: int,
    db: AsyncSession,
    skip_conflicts: bool = False,
) -> ImportResult:
    """
    Import schedule records from an uploaded Excel file.

    Workflow:
      1. Parse the Excel file using the existing excel_parser.
      2. For each row, resolve lab and teacher, validate time slots.
      3. Check for conflicts with existing bookings.
      4. Create LabBookingRequest + LabBookingSlot records.

    Args:
        file_path: Path to the uploaded .xlsx file.
        semester_id: Academic semester to attach bookings to.
        db: Async SQLAlchemy session.
        skip_conflicts: If True, skip rows with conflicts instead of failing.

    Returns:
        ImportResult with created count, skipped count, errors, and warnings.
    """
    result = ImportResult()

    # Validate file exists
    if not os.path.exists(file_path):
        result.errors.append(f"File not found: {file_path}")
        return result

    # Parse Excel
    records, parse_warnings = parse_excel(file_path)
    result.warnings.extend(parse_warnings)

    if not records:
        result.errors.append("No valid records found in file")
        return result

    # Group records by (course, teacher) to batch into single requests
    # Key: (course_name, teacher)
    grouped: Dict[Tuple[str, str], List[Dict]] = {}
    for record in records:
        key = (
            str(record.get("course_name", "")).strip(),
            str(record.get("teacher", "")).strip(),
        )
        grouped.setdefault(key, []).append(record)

    for (course_name, teacher_name), rows in grouped.items():
        try:
            # Resolve teacher
            teacher_id = await _resolve_teacher(teacher_name, db)
            if teacher_id is None:
                result.errors.append(f"Teacher not found: '{teacher_name}'")
                result.skipped += len(rows)
                continue

            # Collect valid slots
            slots_to_create = []
            row_conflict = False

            for row in rows:
                time_info = row.get("time", {})
                day = int(time_info.get("day", 0))
                start = int(time_info.get("start", 0))
                end = int(time_info.get("end", 0))

                # Validate time range
                if not (1 <= day <= 7 and 1 <= start < end <= 12):
                    result.warnings.append(
                        f"Invalid time slot (day={day}, start={start}, end={end}) "
                        f"for course '{course_name}'"
                    )
                    result.skipped += 1
                    continue

                # Resolve lab
                location = str(row.get("location", "")).strip()
                lab_id = await _resolve_lab(location, db)
                if lab_id is None:
                    result.errors.append(
                        f"Lab not found: '{location}' for course '{course_name}'"
                    )
                    result.skipped += 1
                    continue

                # Check conflict — assume week 1 if not specified
                # In practice, week_range parsing should extract weeks
                week = 1
                has_conflict = await check_conflict(lab_id, week, day, start, end, db)

                if has_conflict:
                    if skip_conflicts:
                        result.warnings.append(
                            f"Conflict for {location} week {week} day {day} "
                            f"periods {start}-{end}, skipped"
                        )
                        result.skipped += 1
                        continue
                    else:
                        result.errors.append(
                            f"Conflict for {location} week {week} day {day} "
                            f"periods {start}-{end}"
                        )
                        row_conflict = True
                        break

                # Parse class names (may be comma-separated)
                class_names = str(row.get("classes", "")).strip()

                slots_to_create.append({
                    "lab_id": lab_id,
                    "week_number": week,
                    "day_of_week": day,
                    "period_start": start,
                    "period_end": end,
                    "class_names": class_names,
                })

            if row_conflict:
                continue

            if not slots_to_create:
                result.warnings.append(f"No valid slots for course '{course_name}'")
                continue

            # Create booking request
            request_no = f"REQ-{uuid.uuid4().hex[:8].upper()}"
            all_classes = "; ".join(
                s["class_names"] for s in slots_to_create if s["class_names"]
            )

            booking_request = LabBookingRequest(
                semester_id=semester_id,
                request_no=request_no,
                teacher_id=teacher_id,
                reason="excel_import",
                course_name=course_name,
                class_names=all_classes,
                status="pending",
            )
            db.add(booking_request)
            await db.flush()  # Get the ID

            # Create slots
            for slot_data in slots_to_create:
                slot = LabBookingSlot(
                    lab_id=slot_data["lab_id"],
                    week_number=slot_data["week_number"],
                    day_of_week=slot_data["day_of_week"],
                    period_start=slot_data["period_start"],
                    period_end=slot_data["period_end"],
                    request_id=booking_request.id,
                )
                db.add(slot)

            result.created += len(slots_to_create)

            # Send notification to teacher
            await send_notification(
                db=db,
                user_id=teacher_id,
                type="import_created",
                payload={
                    "request_no": request_no,
                    "course_name": course_name,
                    "slot_count": len(slots_to_create),
                },
            )

        except Exception as e:
            result.errors.append(f"Import error for '{course_name}': {str(e)}")

    # Clean up uploaded file
    try:
        os.remove(file_path)
    except OSError:
        pass

    return result
