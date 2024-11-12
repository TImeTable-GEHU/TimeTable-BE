import random
from constants import TimeInterval

class TimetableFitness:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots  # Using the time_slots from TimeIntervalConstant

        self.subject_teacher_map = {
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
            "PCS-503": ["RS11", "DP07", "SP06", "VD25"]
        }

        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        self.room_schedule = {slot: {} for slot in self.time_slots}
        self.assigned_teachers = {section: {} for section in self.sections}

        # Assign each section to a classroom
        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

        # Define subject weekly quotas
        self.subject_weekly_quota = {
            "TCS-531": 3,
            "TCS-502": 3,
            "TCS-503": 3,
            "PCS-506": 2,
            "PCS-503": 2,
            "TMA-502": 3,
            "PMA-502": 2,
            "TCS-509": 3,
            "XCS-501": 2,
            "CSP-501": 1,
            "SCS-501": 1
        }

        # Track weekly classes assigned to each subject per section
        self.weekly_assignments = {section: {subject: 0 for subject in self.subject_weekly_quota} for section in self.sections}

        # Define ideal weekly workload limits for each teacher
        self.teacher_workload_limits = {
            "AB01": 4, "PK02": 4, "SS03": 4, "AA04": 5, "AC05": 5,
            "SP06": 5, "DP07": 5, "AD08": 4, "RD09": 5, "VD25": 5,
            "RS11": 6, "BJ10": 6, "JM12": 6, "NJ13": 5, "PM14": 6,
            "AA15": 5, "SJ16": 6, "AB17": 5, "HP18": 5, "SG19": 5,
            "DT20": 6, "PA21": 6, "NB22": 6, "AK23": 5, "AP24": 5
        }

        # Define preferred time slots for teachers
        self.preferred_time_slots = {
            "AB01": [1, 2], 
            "PK02": [2, 3],
            "SS03": [3, 4],
            "AA04": [1, 4],
            "AC05": [2, 5],
            "SP06": [1, 3],
            "DP07": [4, 5],
            "AD08": [2, 3],
            "RD09": [1, 5],
            "VD25": [3, 4],
            "RS11": [2, 3],
            "BJ10": [1, 4],
            "JM12": [2, 5],
            "NJ13": [3, 5],
            "PM14": [1, 2],
            "AA15": [4, 5],
            "SJ16": [1, 3],
            "AB17": [2, 4],
            "HP18": [3, 5],
            "SG19": [1, 2],
            "DT20": [4, 5],
            "PA21": [2, 3],
            "NB22": [1, 4],
            "AK23": [3, 5],
            "AP24": [1, 2]
        }

    def generate_day_schedule(self, day, sections_half_day):
        day_schedule = {}
        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]

            # Set time slots for full or half day
            slots_to_run = [1, 2, 3, 4] if section in sections_half_day else list(self.time_slots.keys())

            for index in slots_to_run:
                time_slot = self.time_slots[index]
                
                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None

                # Find an available subject and teacher
                while available_subjects:
                    subject = random.choice(available_subjects)
                    if subject not in subjects_used_today:
                        if subject in self.assigned_teachers[section]:
                            teacher = self.assigned_teachers[section][subject]
                        else:
                            possible_teachers = self.subject_teacher_map[subject]
                            
                            # Try to find a teacher with preferred time slots
                            for possible_teacher in possible_teachers:
                                if possible_teacher in self.preferred_time_slots and index in self.preferred_time_slots[possible_teacher]:
                                    teacher = possible_teacher
                                    break

                            # If no preferred teacher found, pick any available
                            if not teacher:
                                teacher = random.choice(possible_teachers)
                                
                            self.assigned_teachers[section][subject] = teacher
                        break
                    available_subjects.remove(subject)

                # Assign a fallback subject and teacher if none are available
                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"

                # Increment weekly quota for the subject if it's not "Library"
                if subject != "Library":
                    self.weekly_assignments[section][subject] += 1  # Increment the weekly quota for the subject

                subjects_used_today.add(subject)
                self.teacher_schedule[index][teacher] = section
                self.room_schedule[index][current_room] = section

                # Add double-slot handling for lab subjects
                if subject.startswith("PCS") or "Lab" in subject:
                    next_slot_index = index + 1
                    if next_slot_index in slots_to_run:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append({
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": current_room,
                            "time_slot": next_time_slot
                        })

                schedule_item = {
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": current_room,
                    "time_slot": time_slot
                }

                section_schedule.append(schedule_item)
            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self):
        timetable = {}
        for week_day in self.days:
            sections_half_day = random.sample(self.sections, len(self.sections) // 2)
            timetable[week_day] = self.generate_day_schedule(week_day, sections_half_day)
        return timetable

    def print_timetable(self, timetable):
        print("\n--- Weekly Timetable ---\n")
        for day, day_schedule in timetable.items():
            print(f"Day: {day}")
            for section, section_schedule in day_schedule.items():
                print(f"  Section: {section}")
                for item in section_schedule:
                    print(f"    {item['time_slot']}: {item['subject_id']} - {item['teacher_id']} ({item['classroom_id']})")
                print("\n")

# Example usage
fitness = TimetableFitness()
timetable = fitness.create_timetable()
fitness.print_timetable(timetable)
