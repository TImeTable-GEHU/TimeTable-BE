import random
import json
from GA.chromosome import TimetableGeneration
from Constants.constant import (
    WorkingDays,
    Sections,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
    TeacherPreferences,
    PenaltyConstants,
    TeacherWorkLoad,
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
        self.teacher_time_preferences = TeacherPreferences.teacher_preferences
        self.teacher_daily_workload = TeacherWorkLoad.Weekly_workLoad

        # print(self.teacher_daily_workload)

    def evaluate_timetable_fitness(self):
        total_fitness = 0
        daily_section_fitness_scores = {}
        weekly_fitness_scores = {}
        current_week = 1

        # Iterate through the weeks and days of the generated timetable
        for day_index in range(0, len(self.generated_timetable), 5):
            weekly_fitness = 0
            weekly_label = f"Week {current_week}"

            # Iterate through the days in a week
            for day_offset, day_name in enumerate(self.available_days):
                week_day_key = f"Week {current_week} - {day_name}"
                if week_day_key not in self.generated_timetable:
                    continue

                daily_schedule = self.generated_timetable[week_day_key]
                daily_section_fitness_scores[week_day_key] = {}
                day_fitness = 0

                # Iterate through sections for the daily schedule
                for section, section_schedule in daily_schedule.items():
                    section_fitness = 100  # Initial fitness score for each section
                    teacher_time_slot_tracking = {}
                    classroom_time_slot_tracking = {}
                    teacher_workload_tracking = {}

                    # Check each scheduled item for the section
                    for schedule_item in section_schedule:
                        assigned_teacher = schedule_item['teacher_id']
                        assigned_classroom = schedule_item['classroom_id']
                        assigned_time_slot = schedule_item['time_slot']
                        assigned_subject = schedule_item['subject_id']
                        section_strength = self.section_student_strength

                        # Skip breaks
                        if "Break" in assigned_time_slot:
                            continue

                        # Penalty for teacher double-booking
                        if (assigned_teacher, assigned_time_slot) in teacher_time_slot_tracking:
                            section_fitness -= PenaltyConstants.PENALTY_TEACHER_DOUBLE_BOOKED
                        else:
                            teacher_time_slot_tracking[(assigned_teacher, assigned_time_slot)] = section

                        # Penalty for classroom double-booking
                        if (assigned_classroom, assigned_time_slot) in classroom_time_slot_tracking:
                            section_fitness -= PenaltyConstants.PENALTY_CLASSROOM_DOUBLE_BOOKED
                        else:
                            classroom_time_slot_tracking[(assigned_classroom, assigned_time_slot)] = section

                        # Track teacher workload
                        if assigned_teacher not in teacher_workload_tracking:
                            teacher_workload_tracking[assigned_teacher] = []
                        teacher_workload_tracking[assigned_teacher].append(assigned_time_slot)

                        # Check if section strength exceeds classroom capacity
                        if section_strength > self.classroom_capacity:
                            section_fitness -= PenaltyConstants.PENALTY_OVER_CAPACITY

                        # Check if assigned time slot matches teacher preferences
                        preferred_time_slots = self.teacher_time_preferences[assigned_teacher]
                        if assigned_time_slot not in preferred_time_slots:
                            section_fitness -= PenaltyConstants.PENALTY_UN_PREFERRED_SLOT

                    # Penalize teacher overload
                    for teacher, times_assigned in teacher_workload_tracking.items():
                        if len(times_assigned) > self.teacher_daily_workload[teacher]:
                            section_fitness -= PenaltyConstants.PENALTY_OVERLOAD_TEACHER

                    # Store section fitness for the current day and section
                    daily_section_fitness_scores[week_day_key][section] = section_fitness
                    day_fitness += section_fitness

                # Accumulate the total fitness for the week and day
                weekly_fitness += day_fitness
                total_fitness += day_fitness

            # Store weekly fitness scores
            weekly_fitness_scores[weekly_label] = weekly_fitness
            current_week += 1

        # Return the total fitness and the breakdown of daily and weekly fitness
        return total_fitness, daily_section_fitness_scores, weekly_fitness_scores


# Main Execution
if __name__ == "__main__":
    # Set parameters for sections, rooms, and labs
    section_count = 6
    room_count = 8
    lab_count = 3

    # Generate timetable
    timetable_generator = TimetableGeneration(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        section_count=section_count,
        room_count=room_count,
        lab_count=lab_count
    )
    generated_timetable = timetable_generator.create_timetable(5)

    # Debugging: Print the generated timetable structure to check it
    print("Generated Timetable:")
    print(json.dumps(generated_timetable, indent=4))

    # Evaluate timetable fitness
    fitness_evaluator = TimetableFitnessEvaluator(generated_timetable)
    overall_fitness, section_fitness_data, weekly_fitness_data = fitness_evaluator.evaluate_timetable_fitness()

    # Save the generated timetable to a JSON file
    with open("GA/chromosome.json", "w") as timetable_file:
        json.dump(generated_timetable, timetable_file, indent=4)

    # Prepare and save fitness output data
    fitness_output_data = {
        "overall_fitness": overall_fitness,
        "section_fitness_scores": section_fitness_data,
        "weekly_fitness_scores": weekly_fitness_data
    }

    with open("GA/fitness.json", "w") as fitness_scores_file:
        json.dump(fitness_output_data, fitness_scores_file, indent=4)

    # Print overall fitness and indicate saving completion
    print(f"Overall Fitness: {overall_fitness}")
    print("Timetable and fitness scores have been saved.")
