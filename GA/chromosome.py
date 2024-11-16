import random
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import (
    WorkingDays,
    Sections,
    SubjectTeacherMap,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
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

        self.section_rooms = {
            section: self.classrooms[i % len(self.classrooms)]
            for i, section in enumerate(self.sections)
        }

    def generate_day_schedule(self, day, half_day_sections, week_number):
        day_schedule = {}
        subject_teacher_usage = {
            subject: iter(teachers)
            for subject, teachers in self.subject_teacher_map.items()
        }

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

                    if section_subject_count[section][subject] >= self.subject_quota[subject]:
                        available_subjects.remove(subject)
                        continue

                    if subject == "Placement_Class" and index != 6:
                        available_subjects.remove(subject)
                        continue

                    if "Placement_Class" in subject or "PCS" in subject or "PMA" in subject:
                        if index not in [1, 3, 5]:
                            available_subjects.remove(subject)
                            continue
                        is_lab = True

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

                if is_lab:
                    assigned_room = random.choice(self.lab)
                else:
                    assigned_room = current_room

                if is_lab and index + 1 <= num_slots:
                    next_time_slot = self.time_slots[index + 1]
                    section_schedule.append({
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_room,
                        "time_slot": next_time_slot
                    })
                    section_subject_count[section][subject] += 1

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot
                })
                section_subject_count[section][subject] += 1

            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self, num_weeks=5):
        timetable = {}
        for week in range(1, num_weeks + 1):
            for week_day in self.days:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                timetable[f"Week {week} - {week_day}"] = self.generate_day_schedule(week_day, half_day_sections, week)
        return timetable


# Example usage
if __name__ == "__main__":
    generator = TimetableGeneration()
    timetable = generator.create_timetable(num_weeks=2)
    for week_day, schedule in timetable.items():
        print(f"{week_day}: {schedule}")
