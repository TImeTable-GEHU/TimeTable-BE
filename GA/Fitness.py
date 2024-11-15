import random
import json
from GA.chromosome import TimetableGeneration  # Import from GA package

class TimetableFitnessCalculator:
    def __init__(self, timetable):
        self.timetable = timetable
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.teacher_preferences = {
            teacher_id: [1, 2, 3, 4, 5, 6, 7] for teacher_id in [teacher for teachers in timetable.values() for teacher in teachers]
        }
        self.teacher_work_load = {teacher: 5 for teacher in self.teacher_preferences}

    def calculate_fitness(self):
        overall_fitness_score = 0
        section_fitness_scores = {}

        for day, day_schedule in self.timetable.items():
            section_fitness_scores[day] = {}
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
                        section_score -= 30
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section

                    # Penalize if the classroom is assigned multiple sections at the same time
                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 20
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section

                    # Track teacher load to avoid overloading them
                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)

                    # Penalize if the section strength exceeds the classroom capacity
                    if strength > self.room_capacity.get(classroom, 0):
                        section_score -= 25

                    # Penalize if the teacher is assigned to a time slot they don't prefer
                    preferred_slots = self.teacher_preferences.get(teacher, [])
                    if time_slot not in preferred_slots:
                        section_score -= 5

                # Penalize if the teacher exceeds their work load
                for teacher, time_slots in teacher_load.items():
                    if len(time_slots) > self.teacher_work_load.get(teacher, 5):
                        section_score -= 10

                section_fitness_scores[day][section] = section_score
                overall_fitness_score += section_score

        return overall_fitness_score, section_fitness_scores

# Main Execution
# Generate timetable (chromosome) using TimetableGeneration
timetable_generator = TimetableGeneration()
timetable = timetable_generator.create_timetable(2)  # Generate a timetable with 2 weeks

# Now using the new class for fitness calculation
fitness_calculator = TimetableFitnessCalculator(timetable)
overall_fitness, fitness_scores = fitness_calculator.calculate_fitness()

# Save output to a JSON file
output = [
    timetable,
    {"fitness_scores": fitness_scores}
]

# Save the updated fitness score data into the JSON file
with open("GA/Sample_Chromosome_with_fitness.json", "w") as f:
    json.dump(output, f, indent=4)
