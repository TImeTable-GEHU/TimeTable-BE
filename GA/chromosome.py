import random

from Constants.time_intervals import TimeIntervalConstant
from Constants.constant import (
    Sections,
    Classrooms,
    RoomCapacity,
    Defaults
)


class TimeTableGeneration:
    def __init__(
        self,
        teacher_subject_mapping: dict,
        total_sections: int,
        total_classrooms: int,
        total_labs: int,
        teacher_preferences: dict,
        teacher_weekly_workload: dict,
        special_subjects: dict,
        subject_quota_limits: dict,
        labs_list: list,
        teacher_duty_days: dict
    ):
        self.sections_manager = Sections(total_sections)
        self.classrooms_manager = Classrooms(total_classrooms, total_labs)
        self.room_capacity_manager = RoomCapacity(
            self.classrooms_manager.classrooms, self.sections_manager.sections
        )
        self.sections = self.sections_manager.sections
        self.classrooms = self.classrooms_manager.classrooms
        self.lab_classrooms = self.classrooms_manager.labs
        self.room_capacity = self.room_capacity_manager.room_capacity
        self.section_strength = self.room_capacity_manager.section_strength
        self.weekdays = Defaults.working_days
        self.subject_teacher_mapping = teacher_subject_mapping
        self.subject_quota_limits = subject_quota_limits
        self.lab_subject_list = labs_list
        self.special_subject_list = special_subjects
        self.teacher_availability_preferences = teacher_preferences
        self.available_time_slots = TimeIntervalConstant.time_slots
        self.teacher_duty_days = teacher_duty_days
        self.section_to_classroom_map = {
            section: self.classrooms[i % len(self.classrooms)]
            for i, section in enumerate(self.sections)
        }
        self.weekly_workload = teacher_weekly_workload

    def generate_daily_schedule(self, half_day_section_list):
        daily_schedule = {}
        subject_teacher_tracker = {
            subject: iter(teachers) for subject, teachers in self.subject_teacher_mapping.items()
        }
        section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections
        }
        teacher_workload_tracker = {teacher: 0 for teacher in self.weekly_workload.keys()}

        for i, section in enumerate(self.sections):
            section_schedule = []
            subjects_scheduled_today = set()
            assigned_classroom = self.section_to_classroom_map[section]
            total_slots_for_section = 4 if section in half_day_section_list else 7

            # Cycle through weekdays if there are more sections than weekdays
            week_day = self.weekdays[i % len(self.weekdays)]  # Ensure it wraps around
            for slot_index in range(1, total_slots_for_section + 1):
                current_time_slot = self.available_time_slots.get(slot_index)
                if any(schedule_item["time_slot"] == current_time_slot for schedule_item in section_schedule):
                    continue

                available_subjects_for_slot = list(self.subject_teacher_mapping.keys())
                selected_subject, assigned_teacher = None, None
                is_lab_subject = False
                is_special_subject=False

                while available_subjects_for_slot:
                    selected_subject = random.choice(available_subjects_for_slot)

                    # Check if subject quota has been exceeded
                    if section_subject_usage_tracker[section][selected_subject] >= self.subject_quota_limits.get(selected_subject, 0):
                        available_subjects_for_slot.remove(selected_subject)
                        continue

                    # Restrict lab subjects to specific slots
                    if selected_subject in self.lab_subject_list and slot_index not in [1, 3, 5]:
                        available_subjects_for_slot.remove(selected_subject)
                        continue
                    is_lab_subject = selected_subject in self.lab_subject_list
                
                    # Restrict special subjects to specific slots
                    if selected_subject in self.special_subject_list and slot_index not in [5]:
                        available_subjects_for_slot.remove(selected_subject)
                        continue
                    is_special_subject=selected_subject in self.lab_subject_list
                    # Assign teacher if subject is not already scheduled today
                    if selected_subject not in subjects_scheduled_today:
                        teacher_iterator = subject_teacher_tracker[selected_subject]
                        try:
                            potential_teacher = next(teacher_iterator)
                            for week_day in self.weekdays:
                            # Ensure the teacher is available on the current day
                             if week_day not in self.teacher_duty_days.get(potential_teacher, []):
                                continue

                            # Ensure the teacher's workload does not exceed their weekly limit
                            if teacher_workload_tracker[potential_teacher] < self.weekly_workload[potential_teacher]:
                                assigned_teacher = potential_teacher
                                teacher_workload_tracker[assigned_teacher] += 1
                                break
                        except StopIteration:
                            teacher_iterator = iter(self.subject_teacher_mapping[selected_subject])
                            subject_teacher_tracker[selected_subject] = teacher_iterator
                            continue

                        available_subjects_for_slot.remove(selected_subject)

                # Assign placeholder if no suitable subject/teacher is found
                if selected_subject is None or assigned_teacher is None:
                    selected_subject, assigned_teacher = "Library", "None"

                subjects_scheduled_today.add(selected_subject)
                assigned_room = random.choice(self.lab_classrooms) if is_lab_subject else assigned_classroom

                # Handle double-slot allocation for labs
                if is_lab_subject or is_special_subject and slot_index + 1 <= total_slots_for_section:
                    next_time_slot = self.available_time_slots.get(slot_index + 1)
                    section_schedule.append({
                        "teacher_id": assigned_teacher,
                        "subject_id": selected_subject,
                        "classroom_id": assigned_room,
                        "time_slot": next_time_slot,
                    })
                    section_subject_usage_tracker[section][selected_subject] += 1

                # Schedule the current time slot
                section_schedule.append({
                    "teacher_id": assigned_teacher,
                    "subject_id": selected_subject,
                    "classroom_id": assigned_room,
                    "time_slot": current_time_slot,
                })
                section_subject_usage_tracker[section][selected_subject] += 1

            daily_schedule[section] = section_schedule

        return daily_schedule

    def create_timetable(self, num_weeks):
        timetable = {}
        for week in range(1, num_weeks + 1):
            week_schedule = {}
            for week_day in self.weekdays:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                week_schedule[week_day] = self.generate_daily_schedule(half_day_sections)
            timetable[f"Week {week}"] = week_schedule
        return timetable
