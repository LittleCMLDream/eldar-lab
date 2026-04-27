"""Tests for Excel parsing logic."""
from app.services.excel_parser import detect_headers, parse_time_slot

class TestDetectHeaders:
    def test_chinese_headers(self):
        row = ["课程名称", "教师", "班级", "周次", "节次", "地点"]
        result = detect_headers(row)
        assert result["course_name"] == 0
        assert result["teacher_name"] == 1
        assert result["class_names"] == 2
        assert result["time_slots"] == 4

    def test_partial_headers(self):
        row = ["Course", "Teacher", "Unknown"]
        result = detect_headers(row)
        # Should map based on keyword match if added to rules, else empty
        # With current rules, "Course" isn't matched unless "课程" is present
        assert "course_name" not in result

class TestParseTimeSlot:
    def test_numeric_format(self):
        # e.g., "40304" -> day 4, start 3, end 4
        result = parse_time_slot("40304")
        assert result == {"day": 4, "start": 3, "end": 4}

    def test_chinese_format(self):
        result = parse_time_slot("周4 第3-4节")
        assert result == {"day": 4, "start": 3, "end": 4}

    def test_fallback(self):
        result = parse_time_slot("invalid")
        assert result == {"day": 1, "start": 1, "end": 1}
