import random

class Timetable:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = [
            "9:00 - 9:55 A.M",      
            "9:55 - 10:50 A.M", 
            "10:50 - 11:00 A.M (Break)",  
            "11:00 - 11:55 A.M", 
            "11:55 - 12:50 P.M", 
            "12:50 - 1:00 P.M (Lunch Break)",  
            "1:00 - 2:00 P.M"
        ]
        self.teachers = ["T1", "T2", "T3", "T4", "T5"]
        self.subjects = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
        self.classrooms = ["R1", "R2", "R3"]
        self.teacher_subject_map = {
            "T1": ["S1", "S3"],
            "T2": ["S2", "S4", "S6"],
            "T3": ["S2", "S5"],
            "T4": ["S7", "S6"],
            "T5": ["S5", "S1"]
        }
        self.teacher_max_hours = {"T1": 4, "T2": 5, "T3": 4, "T4": 3, "T5": 4}
        self.room_capacity = {"R1": 30, "R2": 25, "R3": 20}
        self.section_strength = {"A": 30, "B": 25, "C": 20, "D": 15}

    def generate_day_schedule(self):
        day_schedule = {}
        time_slot_classroom_usage = {time_slot: set() for time_slot in self.time_slots}
        time_slot_teacher_usage = {time_slot: set() for time_slot in self.time_slots}

        for section in self.sections:
            section_schedule = []
            for time_slot in self.time_slots:
                if "Break" in time_slot:
                    schedule_item = {
                        "teacher_id": "None",
                        "subject_id": "Break",
                        "classroom_id": "N/A",
                        "time_slot": time_slot
                    }
                else:
                    teacher, subject, classroom = None, None, None
                    attempts = 0
                    while attempts < 10:
                        teacher = random.choice(self.teachers)
                        subject = random.choice(self.teacher_subject_map[teacher])
                        classroom = random.choice(self.classrooms)
                        if teacher not in time_slot_teacher_usage[time_slot] and \
                           classroom not in time_slot_classroom_usage[time_slot]:
                            break
                        attempts += 1

                    time_slot_teacher_usage[time_slot].add(teacher)
                    time_slot_classroom_usage[time_slot].add(classroom)

                    schedule_item = {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": classroom,
                        "time_slot": time_slot
                    }
                section_schedule.append(schedule_item)
            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self):
        timetable = {}
        for day in self.days:
            timetable[day] = self.generate_day_schedule()
        return timetable

    def create_multiple_timelines(self, num_chromosomes):
        return [self.create_timetable() for _ in range(num_chromosomes)]

    def calculate_fitness(self, chromosome):
        overall_fitness_score = 0
        section_fitness_scores = {}

        for day, day_schedule in chromosome.items():
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
                    strength = self.section_strength[section]

                    if "Break" in time_slot:
                        continue

                    if (teacher, time_slot) in teacher_time_slots:
                        section_score -= 30  # Penalize for teacher clash
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section

                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 20  # Penalize for classroom clash
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section

                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)

                    if strength > self.room_capacity[classroom]:
                        section_score -= 25

                for teacher, slots in teacher_load.items():
                    if len(slots) > self.teacher_max_hours[teacher]:
                        section_score -= 15

                    for i in range(1, len(slots)):
                        if "Break" not in slots[i - 1] and "Break" not in slots[i]:
                            section_score -= 10  # Penalize if no gaps

                section_fitness_scores[day][section] = max(section_score, 0)
                overall_fitness_score += max(section_score, 0)

        return overall_fitness_score

    def select_custom_parents(self, chromosomes, top_percentage=0.20, random_percentage=0.10):
        """
        Select chromosomes using a combination of the top percentage and some random but good chromosomes for diversity.
        - Select top `top_percentage` of chromosomes based on fitness.
        - Randomly select `random_percentage` of chromosomes for diversity, but from those with good fitness.
        """
        # Calculate fitness scores for each chromosome
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in chromosomes]

        # Sort chromosomes by fitness score in descending order
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Select the top chromosomes (top 20%)
        top_count = max(1, int(len(chromosomes) * top_percentage))  # Ensure at least 1 is selected
        top_chromosomes = [fitness_scores[i][0] for i in range(top_count)]

        # Select the random but good chromosomes (next 10%)
        remaining_chromosomes = [fitness_scores[i][0] for i in range(top_count, len(chromosomes))]
        random_good_count = max(1, int(len(chromosomes) * random_percentage))  # Ensure at least 1 is selected
        random_good_chromosomes = random.sample(remaining_chromosomes, random_good_count)

        # Combine top and random good chromosomes
        selected_chromosomes = top_chromosomes + random_good_chromosomes
        return selected_chromosomes


# Instantiate the Timetable class and generate multiple chromosomes
timetable_obj = Timetable()
num_chromosomes = 10  # Specify the number of chromosomes you want to generate
chromosomes = timetable_obj.create_multiple_timelines(num_chromosomes)

# Calculate fitness for all chromosomes
fitness_scores = [timetable_obj.calculate_fitness(chromosome) for chromosome in chromosomes]

# Select chromosomes using the custom selection method (top 20% + random 10%)
selected_chromosomes = timetable_obj.select_custom_parents(chromosomes, top_percentage=0.20, random_percentage=0.10)

# Display total number of chromosomes and number of selected chromosomes
print(f"\nTotal Number of Chromosomes: {num_chromosomes}")
print(f"Number of Selected Chromosomes (Top 20% + Random 10%): {len(selected_chromosomes)}")

# Display fitness scores in a table
print("\n=== Overall Fitness of All Chromosomes ===")
print(f"{'Chromosome':<15} {'Fitness Score'}")
print("-" * 30)  # Separator
for i, score in enumerate(fitness_scores):
    selected_marker = "*" if chromosomes[i] in selected_chromosomes else " "
    print(f"{f'Chromosome {i + 1}':<15} {score} {selected_marker}")

# Display selected chromosomes
print("\n=== Selected Chromosomes: Top 20% + Random 10% ===")
for i, chromosome in enumerate(selected_chromosomes):
    fitness = timetable_obj.calculate_fitness(chromosome)
    print(f"\n--- Selected Chromosome {i + 1} ---")
    print(f"Overall Fitness Score: {fitness}")
    for day, day_schedule in chromosome.items():
        print(f"\n--- {day} ---")
        print(f"{'Time Slot':<25} {'Teacher':<10} {'Subject':<10} {'Classroom'}")
        print("-" * 60)  # Separator
        for section, schedule in day_schedule.items():
            print(f"Section {section}:")
            for item in schedule:
                print(f"  {item['time_slot']:<25} {item['teacher_id']:<10} {item['subject_id']:<10} {item['classroom_id']}")
            print()  # Extra space after each section
