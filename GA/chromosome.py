import random
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import WorkingDays

class TimetableGeneration:
    def __init__(self):
        self.days = WorkingDays.days
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots

        # Teacher-subject mapping
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
            "PCS-503": ["RS11", "DP07", "SP06", "VD25"],
            "Placement_Class": ["AK26"]
        }

        # Classroom and capacity details
        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.lab = ["L1", "L2", "L3", "L4", "L5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
        
        # Subject weekly quota
        self.subject_quota = {
            "TCS-531": 2, "TCS-502": 3, "TCS-503": 3, "PCS-506": 2, "TMA-502": 2,
            "PMA-502": 2, "TCS-509": 4, "XCS-501": 2, "CSP-501": 1, "SCS-501": 1,
            "PCS-503": 4, "Placement_Class": 1
        }

        # Data structures for tracking schedules
        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

    def generate_day_schedule(self, day, half_day_sections, week_number):
        day_schedule = {}
        subject_teacher_usage = {subject: iter(teachers) for subject, teachers in self.subject_teacher_map.items()}
        
        # Initialize section_subject_count to track the number of times each subject is assigned
        section_subject_count = {
            section: {subject: 0 for subject in self.subject_teacher_map.keys()}
            for section in self.sections
        }

        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]
            num_slots = 4 if section in half_day_sections else 7

            for index in range(1, num_slots + 1):
                time_slot = self.time_slots[index]

                if any(item['time_slot'] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None
                is_lab = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Skip subjects that exceed their weekly quota
                    if section_subject_count[section][subject] >= self.subject_quota[subject]:
                        available_subjects.remove(subject)
                        continue

                    # Handle special rules for Placement_Class and labs
                    if subject == "Placement_Class" and index != 6:
                        available_subjects.remove(subject)
                        continue

                    if "Placement_Class" in subject or "PCS" in subject or "PMA" in subject:
                        if index not in [1, 3, 5]:  # Ensure labs only occupy slots 1, 3, or 5
                            available_subjects.remove(subject)
                            continue
                        is_lab = True  # Mark this as a lab

                    if subject not in subjects_used_today:
                        teacher_iter = subject_teacher_usage[subject]

                        try:
                            teacher = next(teacher_iter)
                        except StopIteration:
                            teacher_iter = iter(self.subject_teacher_map[subject])
                            teacher = next(teacher_iter)
                            subject_teacher_usage[subject] = teacher_iter

                        break

                    available_subjects.remove(subject)

                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"

                subjects_used_today.add(subject)

                # Assign rooms based on whether it's a lab or not
                if is_lab:
                    if subject in ["PCS-506", "PMA-502","PCS-503"]:  # Only PCS or PMA can be assigned to labs
                        assigned_room = random.choice(self.lab)
                    else:
                        assigned_room = current_room
                else:
                    assigned_room = current_room

                # Handle double slot allocation for labs
                if is_lab:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append({
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": assigned_room,
                            "time_slot": next_time_slot
                        })
                        section_subject_count[section][subject] += 1  # Increment subject count for double slot
                    else:
                        continue

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot
                })

                section_subject_count[section][subject] += 1  # Increment subject count for single slot

            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self, num_weeks=5):
        timetable = {}
        for week in range(1, num_weeks + 1):
            for week_day in self.days:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                timetable[f"Week {week} - {week_day}"] = self.generate_day_schedule(week_day, half_day_sections, week)
        return timetable
