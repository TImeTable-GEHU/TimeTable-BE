class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class Sections:
    sections = []

    def __init__(self, section_number):
        self.sections = [chr(65 + i) for i in range(section_number)]


class Classrooms:
    classrooms=0
    labs=0
    def __init__(self, room_count, lab_count):
        # Generate classrooms dynamically: R1, R2, ...
        self.classrooms = [f"R{i + 1}" for i in range(room_count)]
        # Generate labs dynamically: L1, L2, ...
        self.labs = [f"L{i + 1}" for i in range(lab_count)]

class RoomCapacity:
    room_capacity = 0
    section_strength = 0
    def __init__(self, classrooms, sections, default_capacity=200):
        # Initialize capacities for each classroom
        self.room_capacity = {room: default_capacity for room in classrooms}
        # Initialize section strengths for each section
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
    
class TeacherPreferences:
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


class SpecialSubjects:
    special_subjects = ["Placement_Class"]
    Labs=["PCS-506", "PCS-503", "PMA-502","PCS-512"]
    specialization_subjects=["TCS-511","TCS-592","TCS-512","TCS-519","PCS-512"]


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10

"""import requests

class DynamicConstants:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def fetch_data(self, endpoint):
        try:
            response = requests.get(f"{self.backend_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {endpoint}: {e}")
            return {}

class WorkingDays(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.days = self.fetch_data("working_days")  # Example: ["Monday", "Tuesday", ...]

class Sections(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.sections = self.fetch_data("sections")  # Example: ["A", "B", "C", ...]

class Classrooms(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.classrooms = self.fetch_data("classrooms")  # Example: ["R1", "R2", ...]
        self.labs = self.fetch_data("labs")  # Example: ["L1", "L2", ...]

class RoomCapacity(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.room_capacity = self.fetch_data("room_capacity")  # Example: {"R1": 200, "R2": 230, ...}
        self.section_strength = self.fetch_data("section_strength")  # Example: {"A": 200, "B": 200, ...}

class SubjectQuota(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.subject_quota = self.fetch_data("subject_quota")  # Example: {"TCS-531": 3, "TCS-502": 3, ...}

class TeacherPreferences(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.teacher_preferences = self.fetch_data("teacher_preferences")  # Example: {"AB01": [1], ...}

class SpecialSubjects(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.special_subjects = self.fetch_data("special_subjects")  # Example: ["Placement_Class", ...]
        self.labs = self.fetch_data("labs")  # Example: ["PCS-506", "PCS-503", ...]

class PenaltyConstants(DynamicConstants):
    def __init__(self, backend_url):
        super().__init__(backend_url)
        self.constants = self.fetch_data("penalty_constants")  # Example: {"PENALTY_TEACHER_DOUBLE_BOOKED": 30, ...}
        self.PENALTY_TEACHER_DOUBLE_BOOKED = self.constants.get("PENALTY_TEACHER_DOUBLE_BOOKED", 30)
        self.PENALTY_CLASSROOM_DOUBLE_BOOKED = self.constants.get("PENALTY_CLASSROOM_DOUBLE_BOOKED", 20)
        self.PENALTY_OVER_CAPACITY = self.constants.get("PENALTY_OVER_CAPACITY", 25)
        self.PENALTY_UN_PREFERRED_SLOT = self.constants.get("PENALTY_UN_PREFERRED_SLOT", 5)
        self.PENALTY_OVERLOAD_TEACHER = self.constants.get("PENALTY_OVERLOAD_TEACHER", 10)
"""