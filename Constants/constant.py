class Defaults:
    # All the defaults values over GA folder.
    room_capacity = 60
    working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    starting_section_fitness = 100
    max_class_capacity = 250


class Sections:
    sections = []

    def __init__(self, section_number):
        self.sections = [chr(65 + i) for i in range(section_number)]


class Classrooms:
    classrooms = 0
    labs = 0

    def __init__(self, room_count, lab_count):
        self.classrooms = [f"R{i + 1}" for i in range(room_count)]
        self.labs = [f"L{i + 1}" for i in range(lab_count)]


class RoomCapacity:
    room_capacity = 0
    section_strength = 0

    def __init__(self, classrooms, sections, default_capacity=Defaults.room_capacity):
       
        self.room_capacity = {room: default_capacity for room in classrooms}
        self.section_strength = {section: default_capacity for section in sections}


class SubjectQuota:
    subject_quota = {
        "TCS-531": 3,
        "TCS-502": 3,
        "TCS-503": 3,
        "PCS-506": 1,
        "TMA-502": 3,
        "PMA-502": 1,
        "TCS-509": 4,
        "XCS-501": 2,
        "CSP-501": 1,
        "SCS-501": 1,
        "PCS-503": 1,
        "TCS-511":2,
        "TCS-592":2,
        "TCS-512":2,
        "TCS-519":2,
        "PCS-512":1,
        "Placement_Class": 1,
    }


class TeacherPreloads:
    teacher_preferences = {
        "AB01": [1],
        "PK02": [1, 2, 3, 4, 5, 6, 7],
        "SS03": [1, 2, 3, 4, 5, 6, 7],
        "AA04": [1, 2, 3, 4, 5, 6, 7],
        "AC05": [1, 2, 3, 4, 5, 6, 7],
        "SP06": [1, 2, 3, 4, 5, 6, 7],
        "DP07": [1, 2, 3, 4, 5, 6, 7],
        "AD08": [1, 2, 3, 4, 5, 6, 7],
        "RD09": [1, 2, 3, 4, 5, 6, 7],
        "BJ10": [1, 2, 3, 4, 5, 6, 7],
        "RS11": [1, 2, 3, 4, 5, 6, 7],
        "JM12": [1, 2, 3, 4, 5, 6, 7],
        "NJ13": [1, 2, 3, 4, 5, 6, 7],
        "PM14": [1, 2, 3, 4, 5, 6, 7],
        "AA15": [1, 2, 3, 4, 5, 6, 7],
        "SJ16": [1, 2, 3, 4, 5, 6, 7],
        "AB17": [1, 2, 3, 4, 5, 6, 7],
        "HP18": [1, 2, 3, 4, 5, 6, 7],
        "SG19": [1, 2, 3, 4, 5, 6, 7],
        "DT20": [1, 2, 3, 4, 5, 6, 7],
        "PA21": [1, 2, 3, 4, 5, 6, 7],
        "NB22": [1, 2, 3, 4, 5, 6, 7],
        "AK23": [1, 2, 3, 4, 5, 6, 7],
        "AP24": [1, 2, 3, 4, 5, 6, 7],
        "VD25": [1, 2, 3, 4, 5, 6, 7],
        "AK26": [5],
    }

    weekly_workload={
        "AB01": 5,
        "PK02": 5,
        "SS03": 5,
        "AA04": 5,
        "AC05": 5,
        "SP06": 5,
        "DP07": 5,
        "AD08": 5,
        "RD09": 5,
        "BJ10": 5,
        "RS11": 5,
        "JM12": 5,
        "NJ13": 5,
        "PM14": 5,
        "AA15": 5,
        "SJ16": 5,
        "AB17": 5,
        "HP18": 5,
        "SG19": 5,
        "DT20": 5,
        "PA21": 5,
        "NB22": 5,
        "AK23": 5,
        "AP24": 5,
        "VD25": 5,
        "AK26": 5
        }


class SpecialSubjects:
    special_subjects = ["Placement_Class"]
    Labs=["PCS-506", "PCS-503", "PMA-502","PCS-512"]
    # specialization_subjects=["TCS-511","TCS-592","TCS-512","TCS-519","PCS-512"]


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10


class SectionsConstants:
    # Define attribute weights and conditions
    ATTRIBUTE_WEIGHTS = {
        'good_cgpa': 1,         # 2^0
        'hostler': 2,           # 2^1
        # Additional attributes can be added here
    }

    ATTRIBUTE_CONDITIONS = {
        'hostler': lambda student: student.get('Hostler', False),
    }
