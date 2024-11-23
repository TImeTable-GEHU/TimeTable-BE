import json
from GA.chromosome import TimetableGeneration
from Constants.constant import (
    WorkingDays,
    Sections,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
    PenaltyConstants,
    TeacherPreloads,
)
from Samples.samples import SubjectTeacherMap


class TimetableFitnessEvaluator:
    def __init__(self, generated_timetable):
        self.generated_timetable = generated_timetable
        self.available_days = WorkingDays.days
        self.all_sections = Sections.sections
        self.subject_teacher_mapping = SubjectTeacherMap.subject_teacher_map
        self.available_classrooms = Classrooms.classrooms
        self.available_labs = Classrooms.labs
        self.classroom_capacity = RoomCapacity.room_capacity
        self.section_student_strength = RoomCapacity.section_strength
        self.subject_quota_data = SubjectQuota.subject_quota
        self.teacher_time_preferences = TeacherPreloads.teacher_preferences
<<<<<<< HEAD
        self.teacher_daily_workload = TeacherPreloads.weekly_workload
=======
        self.teacher_daily_workload = TeacherWorkLoad.weekly_workload
>>>>>>> 3cc3b2ef4622a16b02dc5828f592ad16e85ffda3

    def evaluate_timetable_fitness(self):
        total_fitness = 0
        daily_section_fitness_scores = {}
        weekly_fitness_scores = {}
        current_week = 1

        for day_index in range(0, len(self.generated_timetable), 5):
            weekly_fitness = 0
            weekly_label = f"Week {current_week}"

            for day_offset, day_name in enumerate(self.available_days):
                week_day_key = f"Week {current_week} - {day_name}"
                if week_day_key not in self.generated_timetable:
                    continue

                daily_schedule = self.generated_timetable[week_day_key]
                daily_section_fitness_scores[week_day_key] = {}
                day_fitness = 0

                for section, section_schedule in daily_schedule.items():
                    section_fitness = 100
                    teacher_time_slot_tracking = {}
                    classroom_time_slot_tracking = {}
                    teacher_workload_tracking = {}

                    for schedule_item in section_schedule:
                        assigned_teacher = schedule_item['teacher_id']
                        assigned_classroom = schedule_item['classroom_id']
                        assigned_time_slot = schedule_item['time_slot']
                        assigned_subject = schedule_item['subject_id']
                        section_strength = self.section_student_strength

                        if "Break" in assigned_time_slot:
                            continue

                        if (assigned_teacher, assigned_time_slot) in teacher_time_slot_tracking:
                            section_fitness -= PenaltyConstants.PENALTY_TEACHER_DOUBLE_BOOKED
                        else:
                            teacher_time_slot_tracking[(assigned_teacher, assigned_time_slot)] = section

                        if (assigned_classroom, assigned_time_slot) in classroom_time_slot_tracking:
                            section_fitness -= PenaltyConstants.PENALTY_CLASSROOM_DOUBLE_BOOKED
                        else:
                            classroom_time_slot_tracking[(assigned_classroom, assigned_time_slot)] = section

                        if assigned_teacher not in teacher_workload_tracking:
                            teacher_workload_tracking[assigned_teacher] = []
                        teacher_workload_tracking[assigned_teacher].append(assigned_time_slot)

                        if section_strength > self.classroom_capacity:
                            section_fitness -= PenaltyConstants.PENALTY_OVER_CAPACITY

                        preferred_time_slots = self.teacher_time_preferences[assigned_teacher]
                        if assigned_time_slot not in preferred_time_slots:
                            section_fitness -= PenaltyConstants.PENALTY_UN_PREFERRED_SLOT

                    for teacher, times_assigned in teacher_workload_tracking.items():
                        if len(times_assigned) > self.teacher_daily_workload[teacher]:
                            section_fitness -= PenaltyConstants.PENALTY_OVERLOAD_TEACHER

                    daily_section_fitness_scores[week_day_key][section] = section_fitness
                    day_fitness += section_fitness

                weekly_fitness += day_fitness
                total_fitness += day_fitness

            weekly_fitness_scores[weekly_label] = weekly_fitness
            current_week += 1

        return total_fitness, daily_section_fitness_scores, weekly_fitness_scores


if __name__ == "__main__":
    total_sections = 6
    total_classrooms = 8
    total_labs = 3

    timetable_generator = TimetableGeneration(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections=total_sections,
        total_classrooms=total_classrooms,
        total_labs=total_labs
    )
    generated_timetable = timetable_generator.create_timetable(5)

    print("Generated Timetable:")
    print(json.dumps(generated_timetable, indent=4))

    fitness_evaluator = TimetableFitnessEvaluator(generated_timetable)
    overall_fitness, section_fitness_data, weekly_fitness_data = fitness_evaluator.evaluate_timetable_fitness()

    with open("GA/chromosome.json", "w") as timetable_file:
        json.dump(generated_timetable, timetable_file, indent=4)

    fitness_output_data = {
        "overall_fitness": overall_fitness,
        "section_fitness_scores": section_fitness_data,
        "weekly_fitness_scores": weekly_fitness_data
    }

    with open("GA/fitness.json", "w") as fitness_scores_file:
        json.dump(fitness_output_data, fitness_scores_file, indent=4)

    print(f"Overall Fitness: {overall_fitness}")
    print("Timetable and fitness scores have been saved.")