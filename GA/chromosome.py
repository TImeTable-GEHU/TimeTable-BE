import random
from Constants.time_intervals import TimeIntervalConstant
from Constants.constant import (
    WorkingDays,
    Sections,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
    TeacherPreferences,
    SpecialSubjects
)

class TimetableGeneration:
    def __init__(self, teacher_subject_mapping: dict, section_count: int, room_count: int, lab_count: int):
        """
        Initialize the timetable generation class with dynamic sections, classrooms, and lab counts.
        """
        # Initialize required components dynamically
        self.sections_obj = Sections(section_count)  # Dynamically generate sections
        self.classrooms_obj = Classrooms(room_count, lab_count)  # Dynamically generate classrooms and labs
        self.room_capacity_obj = RoomCapacity(
            self.classrooms_obj.classrooms, self.sections_obj.sections
        )  # Dynamically assign room capacities

        # Attributes from initialized objects
        self.sections = self.sections_obj.sections
        self.classrooms = self.classrooms_obj.classrooms
        self.lab_rooms = self.classrooms_obj.labs
        self.room_capacity = self.room_capacity_obj.room_capacity
        self.section_strength = self.room_capacity_obj.section_strength

        # Static components
        self.days = WorkingDays.days
        self.subject_teacher_map = teacher_subject_mapping
        self.subject_quota = SubjectQuota.subject_quota
        self.lab_subjects = SpecialSubjects.Labs
        self.special_subjects = SpecialSubjects.special_subjects
        self.teacher_preferences = TeacherPreferences.teacher_preferences
        self.time_slots = TimeIntervalConstant.time_slots

        # Map each section to a classroom in a round-robin fashion
        self.section_rooms = {
            section: self.classrooms[i % len(self.classrooms)]
            for i, section in enumerate(self.sections)
        }

    def generate_day_schedule(self, half_day_sections):
        """
        Generate a schedule for a specific day.

        Args:
            half_day_sections (list): Sections that have a half-day schedule.

        Returns:
            dict: A dictionary representing the day's schedule for all sections.
        """
        day_schedule = {}
        subject_teacher_usage = {
            subject: iter(teachers) for subject, teachers in self.subject_teacher_map.items()
        }

        # Track how often each subject has been assigned to each section
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
                time_slot = self.time_slots.get(index)

                if any(item["time_slot"] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None
                is_lab = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Skip subjects exceeding their weekly quota
                    if section_subject_count[section][subject] >= self.subject_quota.get(subject, 0):
                        available_subjects.remove(subject)
                        continue

                    # Handle lab subject restrictions
                    if subject in self.lab_subjects and index not in [1, 3, 5]:
                        available_subjects.remove(subject)
                        continue
                    is_lab = subject in self.lab_subjects

                    # Handle special subject restrictions
                    if subject in self.special_subjects and index not in [1, 3, 5]:
                        available_subjects.remove(subject)
                        continue

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
                    # Assign a placeholder if no subject/teacher is available
                    subject, teacher = "Library", "None"

                subjects_used_today.add(subject)

                # Assign a room based on whether it's a lab or regular subject
                assigned_room = random.choice(self.lab_rooms) if is_lab else current_room

                # Double-slot handling for labs
                if is_lab and index + 1 <= num_slots:
                    next_time_slot = self.time_slots.get(index + 1)
                    section_schedule.append({
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_room,
                        "time_slot": next_time_slot,
                    })
                    section_subject_count[section][subject] += 1  # Increment for double-slot use

                # Add the current slot's schedule
                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot,
                })
                section_subject_count[section][subject] += 1

            day_schedule[section] = section_schedule

        return day_schedule

    def create_timetable(self, num_weeks=5):
        """
        Create a complete timetable over multiple weeks.

        Args:
            num_weeks (int): Number of weeks for which the timetable is generated.

        Returns:
            dict: A dictionary representing the complete timetable.
        """
        timetable = {}
        for week in range(1, num_weeks + 1):
            for week_day in self.days:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                timetable[f"Week {week} - {week_day}"] = self.generate_day_schedule(half_day_sections)

        return timetable
