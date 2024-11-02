import random

# Define the constraints and available values
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
sections = ["A", "B", "C", "D"]
time_slots = [
    "9:00 - 9:55 A.M",     
    "9:55 - 10:50 A.M",
    "10:50 - 11:00 A.M (Break)",  # Morning Break
    "11:00 - 11:55 A.M",
    "11:55 - 12:50 P.M",
    "12:50 - 1:00 P.M (Lunch Break)",  # Lunch Break
    "1:00 - 2:00 P.M"
]
teachers = ["T1", "T2", "T3", "T4", "T5"]
subjects = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
classrooms = ["R1", "R2", "R3"]

# Teacher-to-subject mappings for constraints
teacher_subject_map = {
    "T1": ["S1", "S3"],
    "T2": ["S2", "S4", "S6"],
    "T3": ["S2", "S5"],
    "T4": ["S7", "S6"],
    "T5": ["S5", "S1"]
}

class TimetableGenerator:
    def __init__(self):
        self.population = []  # Holds the population of chromosomes

    def generate_day_schedule(self):
        """Generate a single day’s timetable for all sections."""
        day_schedule = {}
        for section in sections:
            section_schedule = []
            for time_slot in time_slots:
                # If the time slot is a break or lunch time, add it with no class
                if "Break" in time_slot:
                    schedule_item = {
                        "teacher_id": "None",
                        "subject_id": "Break",
                        "classroom_id": "N/A",
                        "time_slot": time_slot
                    }
                else:
                    # Randomly select a teacher that has available subjects
                    teacher = random.choice(teachers)
                    available_subjects = teacher_subject_map[teacher]
                    subject = random.choice(available_subjects)
                    classroom = random.choice(classrooms)
                    # Construct the schedule item
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
        """Create a full timetable chromosome."""
        timetable = {}
        for day in days:
            timetable[day] = self.generate_day_schedule()
        return timetable

    def calculate_fitness(self, chromosome):
        """Calculate fitness score for a given timetable chromosome."""
        overall_fitness_score = 1000  # Start with a high score for the overall timetable
        section_fitness_scores = {}  # Store fitness scores for each section
        # Constraint 1: No overlap of teachers and classrooms across sections in the same time slot
        for day, day_schedule in chromosome.items():
            section_fitness_scores[day] = {}  # Initialize daily fitness tracking
            for section, section_schedule in day_schedule.items():
                section_score = 100  # Start with a high score for each section
                teacher_time_slots = {}  # Track teachers and their time slots within the section
                classroom_time_slots = {}  # Track classrooms and their time slots within the section
                teacher_load = {}  # Track consecutive slots for each teacher
                for item in section_schedule:
                    teacher = item['teacher_id']
                    classroom = item['classroom_id']
                    time_slot = item['time_slot']
                    if "Break" in time_slot:
                        continue  # Skip breaks
                    # Check for teacher overlap
                    if (teacher, time_slot) in teacher_time_slots:
                        section_score -= 30  # Heavier penalty for teacher overlap
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section
                    # Check for classroom overlap
                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 20  # Heavier penalty for classroom overlap
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section
                    # Track teacher load to ensure no consecutive slots without breaks
                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)
                # Penalty for teachers having back-to-back slots without breaks
                for teacher, slots in teacher_load.items():
                    for i in range(1, len(slots)):
                        if "Break" not in slots[i - 1] and "Break" not in slots[i]:
                            section_score -= 10  # Penalty for consecutive classes without a break
                # Introduce a random variation in the section base score
                section_score += random.randint(-20, 20)  # Adds more score range variability
                # Store the fitness score for this section
                section_fitness_scores[day][section] = max(section_score, 0)  # Ensure non-negative
                overall_fitness_score += section_score - 100  # Adjust overall fitness
        # Ensure fitness is non-negative
        overall_fitness_score = max(overall_fitness_score, 0)
        return overall_fitness_score

    def tournament_selection(self, tournament_size=3):
        """Select a parent chromosome using tournament selection."""
        tournament = random.sample(self.population, tournament_size)  # Randomly select individuals for the tournament
        tournament_fitness = [self.calculate_fitness(chromosome) for chromosome in tournament]
        winner_index = tournament_fitness.index(max(tournament_fitness))  # Find the index of the best fitness
        return tournament[winner_index]  # Return the best chromosome

    def roulette_wheel_selection(self):
        """Select a parent chromosome using roulette wheel selection."""
        total_fitness = sum(self.calculate_fitness(chromosome) for chromosome in self.population)
        selection_probs = [self.calculate_fitness(chromosome) / total_fitness for chromosome in self.population]
        random_value = random.random()
        cumulative_probability = 0.0
        for index, prob in enumerate(selection_probs):
            cumulative_probability += prob
            if random_value <= cumulative_probability:
                return self.population[index]  # Return the selected chromosome

    def rank_selection(self):
        """Select a parent chromosome using rank selection."""
        sorted_population = sorted(self.population, key=self.calculate_fitness, reverse=True)  # Sort by fitness
        rank_probs = [(i + 1) / len(sorted_population) for i in range(len(sorted_population))]  # Calculate rank probabilities
        random_value = random.random()
        cumulative_probability = 0.0
        for index, prob in enumerate(rank_probs):
            cumulative_probability += prob
            if random_value <= cumulative_probability:
                return sorted_population[index]  # Return the selected chromosome

    def assess_selection_algorithms(self, runs=5):
        """Assess the performance of different selection algorithms over multiple runs."""
        results = {
            'tournament': [],
            'roulette': [],
            'rank': []
        }

        # Create an initial population
        self.population = [self.create_timetable() for _ in range(10)]  # Keeping population size at 10

        # Run each selection method 'runs' times
        for _ in range(runs):
            # Tournament Selection
            selected_chromosome = self.tournament_selection()
            fitness_score = self.calculate_fitness(selected_chromosome)
            results['tournament'].append(fitness_score)

            # Roulette Wheel Selection
            selected_chromosome = self.roulette_wheel_selection()
            fitness_score = self.calculate_fitness(selected_chromosome)
            results['roulette'].append(fitness_score)

            # Rank Selection
            selected_chromosome = self.rank_selection()
            fitness_score = self.calculate_fitness(selected_chromosome)
            results['rank'].append(fitness_score)

        # Calculate average scores
        average_scores = {method: sum(scores) / runs for method, scores in results.items()}
        
        # Find the best selection method
        best_method = max(average_scores, key=average_scores.get)
        best_score = average_scores[best_method]

        print("\n--- Average Fitness Scores ---")
        for method, avg_score in average_scores.items():
            print(f"{method.capitalize()} Selection: {avg_score:.2f}")

        print(f"\nBest Selection Method: {best_method.capitalize()} with an average score of {best_score:.2f}")

    def run(self):
        """Run the timetable generator and assess selection methods."""
        self.assess_selection_algorithms(runs=5)

# Create an instance of the TimetableGenerator and run the assessment
timetable_gen = TimetableGenerator()
timetable_gen.run()
