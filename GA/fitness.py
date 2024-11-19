import random
import json
from GA.chromosome import TimetableGeneration  # Import from GA package
from Constants.constant import (
    WorkingDays,
    Sections,
    SubjectTeacherMap,
    Classrooms,
    RoomCapacity,
    SubjectQuota,
    TeacherPreferences, PenaltyConstants
)


class TimetableFitnessCalculator:
    def __init__(self, timetable):
        self.timetable = timetable
        self.section_strength = Sections.sections
        self.days = WorkingDays.days
        self.sections = Sections.sections
        self.subject_teacher_map = SubjectTeacherMap.subject_teacher_map
        self.classrooms = Classrooms.classrooms
        self.lab = Classrooms.labs
        self.room_capacity = RoomCapacity.room_capacity
        self.section_strength = RoomCapacity.section_strength
        self.subject_quota = SubjectQuota.subject_quota
        self.teacher_preferences = TeacherPreferences.teacher_preferences
        self.teacher_work_load = {teacher: 5 for teacher in self.subject_teacher_map.keys()} 

    def calculate_fitness(self):
        total_fitness_score = 0
        section_fitness_scores = {}
        weekly_fitness_scores = {}
        week_count = 1

        for i in range(0, len(self.timetable), 5):  # Assuming 5 days per week
            weekly_score = 0
            weekly_name = f"Week {week_count}"

            for j, day in enumerate(self.days):
                day_schedule = self.timetable.get(f"Week {week_count} - {day}")
                if not day_schedule:
                    continue

                section_fitness_scores[f"Week {week_count} - {day}"] = {}
                daily_fitness_score = 0

                for section, section_schedule in day_schedule.items():
                    section_score = 100
                    teacher_time_slots = {}
                    classroom_time_slots = {}
                    teacher_load = {}

                    for item in section_schedule:
                        teacher = item['teacher_id']
                        classroom = item['classroom_id']
                        time_slot = item['time_slot']
                        subject = item['subject_id']
                        strength = self.section_strength.get(section, 0)

                        if "Break" in time_slot:
                            continue

                        # Penalize if the teacher is assigned multiple sections at the same time
                        if (teacher, time_slot) in teacher_time_slots:
                            section_score -= PenaltyConstants.PENALTY_TEACHER_DOUBLE_BOOKED
                        else:
                            teacher_time_slots[(teacher, time_slot)] = section

                        # Penalize if the classroom is assigned multiple sections at the same time
                        if (classroom, time_slot) in classroom_time_slots:
                            section_score -= PenaltyConstants.PENALTY_CLASSROOM_DOUBLE_BOOKED
                        else:
                            classroom_time_slots[(classroom, time_slot)] = section

                        # Track teacher load to avoid overloading them
                        if teacher not in teacher_load:
                            teacher_load[teacher] = []
                        teacher_load[teacher].append(time_slot)

                        # Penalize if the section strength exceeds the classroom capacity
                        if strength > self.room_capacity.get(classroom, 0):
                            section_score -= PenaltyConstants.PENALTY_OVER_CAPACITY

                        # Penalize if the teacher is assigned to a time slot they don't prefer
                        preferred_slots = self.teacher_preferences.get(teacher, [])
                        if time_slot not in preferred_slots:
                            section_score -= PenaltyConstants.PENALTY_UN_PREFERRED_SLOT

                    # Penalize if the teacher exceeds their work load
                    for teacher, time_slots in teacher_load.items():
                        if len(time_slots) > self.teacher_work_load.get(teacher, 5):
                            section_score -= PenaltyConstants.PENALTY_OVERLOAD_TEACHER

                    section_fitness_scores[f"Week {week_count} - {day}"][section] = section_score
                    daily_fitness_score += section_score

                weekly_score += daily_fitness_score  # Accumulate weekly score
                total_fitness_score += daily_fitness_score

            weekly_fitness_scores[weekly_name] = weekly_score  # Store weekly score
            week_count += 1

        return total_fitness_score, section_fitness_scores, weekly_fitness_scores


# Main Execution
# Generate timetable (chromosome) using TimetableGeneration
timetable_generator = TimetableGeneration()
timetable = timetable_generator.create_timetable(5)  # Generate a timetable with 2 weeks

# Now using the new class for fitness calculation
fitness_calculator = TimetableFitnessCalculator(timetable)
overall_fitness, fitness_scores, weekly_fitness_scores = fitness_calculator.calculate_fitness()

# Save the timetable (chromosome) to a JSON file
with open("GA/chromosome.json", "w") as chromosome_file:
    json.dump(timetable, chromosome_file, indent=4)

# Save the fitness scores to a separate JSON file
fitness_output = {
    "fitness_scores": fitness_scores,
    "weekly_fitness_scores": weekly_fitness_scores
}

with open("GA/fitness.json", "w") as fitness_file:
    json.dump(fitness_output, fitness_file, indent=4)