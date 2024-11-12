import random
from constants.TimeIntervals import TimeIntervalConstant

class TimetableFitness:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots

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

        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        self.room_schedule = {slot: {} for slot in self.time_slots}
        self.assigned_teachers = {section: {} for section in self.sections}

        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

        self.subject_weekly_quota = {
            "TCS-531": 3,
            "TCS-502": 3,
            "TCS-503": 3,
            "PCS-506": 1,
            "PCS-503": 1,
            "TMA-502": 3,
            "PMA-502": 1,
            "TCS-509": 3,
            "XCS-501": 2,
            "CSP-501": 1,
            "SCS-501": 1,
            "Placement_Class": 1  
        }

        self.weekly_assignments = {section: {subject: 0 for subject in self.subject_weekly_quota} for section in self.sections}

        # Add teacher preferences: A dictionary with teacher ID as key and preferred time slots as values
        self.teacher_preferences = {
    "AB01": [1, 2, 3, 4, 5, 6, 7],
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
    "AK26": [1, 2, 3, 4, 5, 6, 7]
}


        # Store teacher assignments for each subject per section
        self.teacher_assignments = {}

    def generate_day_schedule(self, day, half_day_sections, week_number):
        day_schedule = {}
        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]

            if section in half_day_sections:
                num_slots = 4  # Half day: Only 4 slots
            else:
                num_slots = 7  # Full day: 7 slots

            for index in range(1, num_slots + 1):
                time_slot = self.time_slots[index]

                # Check if slot is already used for this section
                if any(item['time_slot'] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None

                # Find an available subject and teacher
                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Ensure "Placement_Class" is only assigned to time slot 6
                    if subject == "Placement_Class" and index != 6:
                        available_subjects.remove(subject)
                        continue

                    # Skip lab subjects if not in allowed slots
                    if ("PCS" in subject or "PMA" in subject or "Lab" in subject) and index not in [1, 3, 5]:
                        available_subjects.remove(subject)
                        continue

                    if subject not in subjects_used_today:
                        # Get the teacher for the subject
                        possible_teachers = self.subject_teacher_map[subject]
                        
                        # Check teacher assignments for this week
                        if week_number > 1 and subject in self.teacher_assignments.get(section, {}):
                            # Use the teacher already assigned to this subject for the section
                            teacher = self.teacher_assignments[section][subject]
                            break

                        # Try to assign the teacher to their preferred time slot
                        for teacher in possible_teachers:
                            preferred_slots = self.teacher_preferences.get(teacher, [])
                            if index in preferred_slots and time_slot not in self.teacher_schedule[index]:
                                self.assigned_teachers[section][subject] = teacher
                                self.teacher_assignments.setdefault(section, {})[subject] = teacher  # Store the teacher assignment
                                break
                        else:
                            # If no preferred slot found, assign the teacher randomly
                            teacher = random.choice(possible_teachers)
                            self.assigned_teachers[section][subject] = teacher
                            self.teacher_assignments.setdefault(section, {})[subject] = teacher  # Store the teacher assignment
                        break

                    available_subjects.remove(subject)

                # Default subject and teacher if none found
                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"

                if subject != "Library":
                    self.weekly_assignments[section][subject] += 1

                subjects_used_today.add(subject)
                self.teacher_schedule[index][teacher] = section
                self.room_schedule[index][current_room] = section

                # Double-slot handling for lab subjects
                if ("PCS" in subject or "PMA" in subject or "Lab" in subject) and index in [1, 3, 5]:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append({
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": current_room,
                            "time_slot": next_time_slot
                        })
                        self.room_schedule[next_slot_index][current_room] = section
                        self.teacher_schedule[next_slot_index][teacher] = section

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": current_room,
                    "time_slot": time_slot
                })
            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self, num_weeks=1):
        timetable = {}
        for week in range(1, num_weeks + 1):
            for week_day in self.days:
                # Randomly select half-day sections
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                timetable[f"Week {week} - {week_day}"] = self.generate_day_schedule(week_day, half_day_sections, week)
        return timetable

    def print_timetable(self, timetable):
        print("\n--- Weekly Timetable ---\n")
        for day, day_schedule in timetable.items():
            print(f"Day: {day}")
            for section, section_schedule in day_schedule.items():
                print(f"  Section: {section}")
                for item in section_schedule:
                    print(f"    {item['time_slot']}: {item['subject_id']} (Teacher: {item['teacher_id']}, Room: {item['classroom_id']})")
                print("  " + "-"*40)
            print("="*60)

# Usage:
fitness = TimetableFitness()
timetable = fitness.create_timetable(num_weeks=1)  # Example: Create timetable for 2 weeks
fitness.print_timetable(timetable)
