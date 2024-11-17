class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class Sections:
    sections = ["A", "B", "C", "D"]

class TimeIntervalConstant:
    time_slots = {
        1: "9:00 - 9:55",
        2: "9:55 - 10:50",
        3: "11:10 - 12:05",
        4: "12:05 - 1:00",
        5: "1:20 - 2:15",
        6: "2:15 - 3:10",
        7: "3:30 - 4:25",
    }

    @staticmethod
    def get_slot(slot_number: int) -> str:
        """Retrieve time slot based on slot number.

        Args:
            slot_number (int): The slot number corresponding to a time interval.

        Returns:
            str: The time interval for the given slot number.

        Raises:
            ValueError: If the slot number is out of the valid range.
        """

        if slot_number in TimeIntervalConstant.time_slots:
            return TimeIntervalConstant.time_slots[slot_number]

        else:
            max_slot = len(TimeIntervalConstant.time_slots)
            raise ValueError(f"Invalid slot number. Please provide a slot number between 1 and {max_slot + 1}.")


    @classmethod
    def get_slot_number(cls, start_time: str, end_time: str):
        """Get the slot number for a given start and end time.

        Args:
            start_time (str): The start time in "HH:MM" format.
            end_time (str): The end time in "HH:MM" format.

        Returns:
            int or str: The slot number if found; otherwise, returns an error message.
        """

        try:
            # Format start and end times to ensure they only include hours and minutes
            start_time = str(datetime.strptime(start_time, "%H:%M").time())
            end_time = str(datetime.strptime(end_time, "%H:%M").time())

            for slot, interval in cls.time_slots.items():
                # Making string in this format: "3:30 - 4:25".
                slot_start_time = datetime.strptime(interval.split(" - ")[0], "%H:%M").time()
                slot_end_time = datetime.strptime(interval.split(" - ")[1], "%H:%M").time()

                if start_time == slot_start_time and end_time == slot_end_time:
                    return slot
            raise LookupError("No Time slot for this time interval found!")

        except ValueError:
            raise ValueError("Invalid time format!")

    @staticmethod
    def get_all_slot_numbers():
        """Retrieve all slot numbers."""
        return list(TimeIntervalConstant.time_slots.keys())

    @staticmethod
    def get_all_time_slots():
        """Retrieve all time intervals."""
        return list(TimeIntervalConstant.time_slots.values())

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
        "AK26": [1, 2, 3, 4, 5, 6, 7],
    }
  