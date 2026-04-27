import pandas as pd
HEADER_RULES = {
    "course_name": ["课程名称", "课程"], "teacher_name": ["教师"],
    "class_names": ["班级"], "week_range": ["周次"],
    "time_slots": ["节次"], "location": ["地点"]
}
def detect_headers(row):
    mapping = {}
    for i, val in enumerate(row):
        for field, kws in HEADER_RULES.items():
            if any(k in str(val) for k in kws):
                mapping[field] = i
                break
    return mapping
def parse_excel(df):
    # 1. Remove header row
    data = df.iloc[1:].copy()
    # 2. Ffill merged cells
    if 1 in data.columns: data[1] = data[1].ffill()
    # 3. Drop empty
    data = data.dropna(how='all')
    return data