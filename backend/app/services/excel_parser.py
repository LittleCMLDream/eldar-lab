import pandas as pd
import re
from typing import List, Dict, Tuple

HEADER_RULES = {
    "course_name": ["课程名称", "课程名", "课程"],
    "teacher_name": ["教师", "任课教师"],
    "class_names": ["班级", "授课班级"],
    "week_range": ["周次", "教学周"],
    "time_slots": ["节次", "时间"],
    "location": ["地点", "教室", "实验室"]
}

def detect_headers(row) -> Dict[str, int]:
    mapping = {}
    for i, val in enumerate(row):
        val_str = str(val).strip()
        for field, kws in HEADER_RULES.items():
            if any(k in val_str for k in kws):
                mapping[field] = i
                break
    return mapping

def parse_time_slot(raw: str) -> Dict[str, int]:
    raw = str(raw).strip()
    
    # 策略 1: 连续数字格式，如 "40304" -> 4-03-04 -> 周4 第3-4节
    # 或者 "30102" -> 3-01-02 -> 周3 第1-2节
    # 假设格式: [Day][Start][End] 但可能有 0 填充
    match = re.match(r'^(\d)(\d{2})(\d{2})$', raw)
    if match:
        return {
            "day": int(match.group(1)),
            "start": int(match.group(2)),
            "end": int(match.group(3))
        }
        
    # 策略 2: 提取所有数字 (备选)
    digits = [int(d) for d in re.findall(r'\d+', raw)]
    if len(digits) >= 3:
        # 尝试解析为 [Day, Start, End]
        return {"day": digits[0], "start": digits[1], "end": digits[2]}
        
    # 策略 3: 中文格式 "周4 3-4节"
    match = re.search(r'周\s*(\d).*?(\d+)-(\d+)', raw)
    if match:
        return {"day": int(match.group(1)), "start": int(match.group(2)), "end": int(match.group(3))}
    
    # Fallback
    return {"day": 1, "start": 1, "end": 1}

def parse_excel(file_path: str) -> Tuple[List[Dict], List[str]]:
    try:
        df = pd.read_excel(file_path)
        if df.empty: return [], ["Empty file"]
        
        header_map = detect_headers(df.iloc[0])
        if not header_map: return [], ["Header detection failed"]
        
        data = df.iloc[1:].copy()
        if 1 in data.columns: data[1] = data[1].ffill()
        data = data[~data[0].astype(str).str.contains('合计', na=False)]
        
        records = []
        warnings = []
        for idx, row in data.iterrows():
            try:
                time_info = parse_time_slot(row.get(header_map.get('time_slots', -1), ''))
                records.append({
                    "course_name": row.get(header_map.get('course_name', -1), ''),
                    "teacher": row.get(header_map.get('teacher_name', -1), ''),
                    "classes": row.get(header_map.get('class_names', -1), ''),
                    "time": time_info,
                    "location": row.get(header_map.get('location', -1), '')
                })
            except Exception as e:
                warnings.append(f"Row {idx} error: {str(e)}")
        return records, warnings
    except Exception as e:
        return [], [f"File read error: {str(e)}"]
