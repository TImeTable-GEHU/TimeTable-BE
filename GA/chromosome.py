import random
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import (
    WorkingDays,
    Sections,
    SubjectTeacherMap,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
    TeacherPreferences,
    SpecialSubjects
)


class TimetableGeneration:
    def __init__(self):
        self.days = WorkingDays.days
        self.sections = Sections.sections
        self.subject_teacher_map = SubjectTeacherMap.subject_teacher_map
        self.classrooms = Classrooms.classrooms
        self.lab = Classrooms.labs
        self.room_capacity = RoomCapacity.room_capacity
        self.section_strength = RoomCapacity.section_strength
        self.subject_quota = SubjectQuota.subject_quota
        self.time_slots = TimeIntervalConstant.time_slots
        self.teacher_preferences = TeacherPreferences.teacher_preferences
        self.special_subjects = SpecialSubjects.special_subjects

        # Map each section to a classroom in a round-robin fashion
        self.section_rooms = {
            section: self.classrooms[i % len(self.classrooms)]
            for i, section in enumerate(self.sections)
        }

    def generate_day_schedule(self, week_day, half_day_sections, weekly_subject_count):
        day_schedule = {}
        subject_teacher_usage = {
            subject: iter(teachers)
            for subject, teachers in self.subject_teacher_map.items()
        }

        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]
            num_slots = 4 if section in half_day_sections else 7  # Half-day or full-day schedule

            index = 1  # Start from the first time slot
            while index <= num_slots:
                time_slot = self.time_slots[index]

                # Skip if a schedule for the time slot already exists
                if any(item['time_slot'] == time_slot for item in section_schedule):
                    index += 1
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None
                is_lab = False
                requires_two_slots = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Check if the subject's weekly quota has been exceeded
                    if weekly_subject_count[section][subject] >= self.subject_quota.get(subject, 0):
                        available_subjects.remove(subject)
                        continue

                    # Check if the subject is a special subject and needs a lab
                    if subject in self.special_subjects:
                        if index not in [1, 3, 5]:  # Special subjects only allowed in specific slots
                            available_subjects.remove(subject)
                            continue
                        is_lab = True
                        requires_two_slots = True

                    if subject not in subjects_used_today:
                        teacher_iter = subject_teacher_usage[subject]

                        try:
                            teacher = next(teacher_iter)
                        except StopIteration:
                            teacher_iter = iter(self.subject_teacher_map[subject])
                            teacher = next(teacher_iter)
                            subject_teacher_usage[subject] = teacher_iter

                        # Check teacher's time slot preferences
                        preferred_slots = self.teacher_preferences.get(teacher, [])
                        if time_slot not in preferred_slots:
                            available_subjects.remove(subject)
                            continue

                        break

                    available_subjects.remove(subject)

                # If no subject or teacher is available, assign "Library"
                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"
                    requires_two_slots = False  # Library doesn't need consecutive slots

                assigned_room = random.choice(self.lab) if is_lab else current_room

                # Add the schedule for the time slot
                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot
                })

                # Handle special subjects requiring two consecutive slots
                if requires_two_slots and index + 1 <= num_slots:
                    next_time_slot = self.time_slots[index + 1]
                    section_schedule.append({
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_room,
                        "time_slot": next_time_slot
                    })
                    index += 1  # Skip the next slot since it's already used

                # Update the weekly subject count for non-Library subjects
                if subject != "Library":
                    weekly_subject_count[section][subject] += 1
                    subjects_used_today.add(subject)

                # Move to the next slot
                index += 1

            # Store the schedule for this section
            day_schedule[section] = section_schedule

        return day_schedule

    def create_timetable(self, num_weeks=5):
        timetable = {}

        for week in range(1, num_weeks + 1):
            weekly_subject_count = {
                section: {subject: 0 for subject in self.subject_teacher_map.keys()}
                for section in self.sections
            }

            for week_day in self.days:
                # Randomly select sections that have a half-day schedule
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                day_schedule = self.generate_day_schedule(week_day, half_day_sections, weekly_subject_count)
                timetable[f"Week {week} - {week_day}"] = day_schedule

        return timetable
