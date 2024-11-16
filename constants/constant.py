class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class Sections:
    sections = ["A", "B", "C", "D"]


class SubjectTeacherMap:
    subject_teacher_map = {
        "TCS-531": ["AB01", "PK02"],
        "TCS-502": ["SS03", "AA04", "AC05"],
        "TCS-503": ["SP06", "DP07", "AC05"],
        "PCS-506": ["AD08", "RD09"],
        "TMA-502": ["BJ10", "RS11", "JM12", "NJ13"],
        "PMA-502": ["PM14", "AD08", "AA15"],
        "TCS-509": ["SJ16", "AB17", "HP18", "SG19"],
        "XCS-501": ["DT20", "PA21", "NB22"],
        "CSP-501": ["AK23"],
        "SCS-501": ["AP24"],
        "PCS-503": ["RS11", "DP07", "SP06", "VD25"],
        "Placement_Class": ["AK26"],
    }


class Classrooms:
    classrooms = ["R1", "R2", "R3", "R4", "R5"]
    labs = ["L1", "L2", "L3", "L4", "L5"]


class RoomCapacity:
    room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
    section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}


class SubjectQuota:
    subject_quota = {
        "TCS-531": 2,
        "TCS-502": 3,
        "TCS-503": 3,
        "PCS-506": 2,
        "TMA-502": 2,
        "PMA-502": 2,
        "TCS-509": 4,
        "XCS-501": 2,
        "CSP-501": 1,
        "SCS-501": 1,
        "PCS-503": 4,
        "Placement_Class": 1,
    }