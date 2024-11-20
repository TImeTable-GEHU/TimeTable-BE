import random
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import WorkingDays


class Chromosome:
    def __init__(self):
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots
        self.days = WorkingDays.days
        self.subject_teacher_map = {
            "TCS-531": ["AB01", "PK02"],
            "TCS-502": ["SS03", "AA04", "AC05"],
            "TCS-503": ["SP06", "DP07", "AC05"],
            "PCS-506": ["AD08", "RD09"],
            "TMA-502": ["BJ10", "RS11", "JM12", "NJ13"],
            "PMA-502": ["PM14", "AD08", "AA15"],
            "TCS-509": ["SJ16", "AB17", "HP18", "SG19"],
            "XCS-501": ["DT20", "PA21", "NB22"],
            "CSP-501": ["AK23"],
            "SCS-501": ["AP24"]
        }
        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}

    def create_chromosome(self):
        schedule = {}
        teacher_schedule = {slot: {} for slot in self.time_slots}
        room_schedule = {slot: {} for slot in self.time_slots}

        for day in self.days:
            schedule[day] = {}
            for section in self.sections:
                schedule[day][section] = []
                for time_slot in self.time_slots:
                    subject = random.choice(list(self.subject_teacher_map.keys()))
                    teacher = random.choice(self.subject_teacher_map[subject])
                    classroom = random.choice(self.classrooms)

                    if (teacher not in teacher_schedule[time_slot] and
                            section not in room_schedule[time_slot].get(classroom, [])):
                        entry = {
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": classroom,
                            "time_slot": time_slot
                        }
                        schedule[day][section].append(entry)
                        teacher_schedule[time_slot][teacher] = True
                        if classroom not in room_schedule[time_slot]:
                            room_schedule[time_slot][classroom] = []
                        room_schedule[time_slot][classroom].append(section)
        return schedule

    def create_multiple_chromosomes(self, num_chromosomes):
        chromosomes = []
        for _ in range(num_chromosomes):
            chromosomes.append(self.create_chromosome())
        return chromosomes

    def crossover(self, parent1, parent2):
        """Perform single-point crossover on two parent chromosomes."""
        offspring1 = {}
        offspring2 = {}

        days = self.days
        crossover_point = random.randint(1, len(days) - 1)

        for i, day in enumerate(days):
            if i < crossover_point:
                offspring1[day] = parent1[day]
                offspring2[day] = parent2[day]
            else:
                offspring1[day] = parent2[day]
                offspring2[day] = parent1[day]

        return offspring1, offspring2

    def mutate_timetable(self, chromosome, mutation_rate=0.7):
        """Applies mutation to a timetable chromosome."""
        classrooms = self.classrooms
        sections = self.sections
        mutated_chromosome = chromosome.copy()

        for day, section_schedule in mutated_chromosome.items():
            for section, entries in section_schedule.items():
                for entry in entries:
                    if random.random() < mutation_rate:
                        entry["time_slot"] = random.choice(self.time_slots)
                        entry["classroom_id"] = random.choice(classrooms)
                        entry["section"] = random.choice(sections)

        return mutated_chromosome

    def create_population_with_crossover_and_mutation(self, parent_chromosomes, num_offspring, mutation_rate=0.7):
        """Generate offspring using crossover and mutation from parent chromosomes."""
        offspring = []
        while len(offspring) < num_offspring:
            parent1, parent2 = random.sample(parent_chromosomes, 2)
            child1, child2 = self.crossover(parent1, parent2)

            child1 = self.mutate_timetable(child1, mutation_rate)
            child2 = self.mutate_timetable(child2, mutation_rate)

            offspring.append(child1)
            if len(offspring) < num_offspring:
                offspring.append(child2)

        return offspring

    def print_chromosomes(self, chromosomes):
        for idx, chromosome in enumerate(chromosomes, 1):
            print(f"\nChromosome {idx}:")
            for day, sections in chromosome.items():
                print(f"  {day}:")
                for section, schedule in sections.items():
                    print(f"    Section {section}:")
                    for entry in schedule:
                        print(f"      Time Slot: {entry['time_slot']}")
                        print(f"        Teacher ID: {entry['teacher_id']}")
                        print(f"        Subject ID: {entry['subject_id']}")
                        print(f"        Classroom ID: {entry['classroom_id']}")
                        print()


if __name__ == "__main__":
    chromosome_constant = Chromosome()
    num_parents = 4
    num_offspring = 6

    parent_chromosomes = chromosome_constant.create_multiple_chromosomes(num_parents)
    print("Parent Chromosomes:")
    chromosome_constant.print_chromosomes(parent_chromosomes)

    offspring = chromosome_constant.create_population_with_crossover_and_mutation(parent_chromosomes, num_offspring)
    print("\nOffspring Chromosomes:")
    chromosome_constant.print_chromosomes(offspring)
