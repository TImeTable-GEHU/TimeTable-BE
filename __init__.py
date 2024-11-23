# This is the Orchestrator file, which will govern the flow.
from Constants.constant import Defaults
from GA.selection import TimeTableSelection
from GA.fitness import TimetableFitnessEvaluator
from GA.chromosome import TimeTableGeneration
from Samples.samples import SubjectTeacherMap


# Create Chromosomes
def run_timetable_generation():
    timetable_generator = TimeTableGeneration(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections=6,
        total_classrooms=8,
        total_labs=3
    )
    timetable = timetable_generator.create_timetable()


    # Fitness of each Chromosome
    fitness_calculator = TimetableFitnessEvaluator(
        timetable,
        timetable_generator.sections,
        SubjectTeacherMap.subject_teacher_map,
        timetable_generator.classrooms,
        timetable_generator.lab_classrooms,
        timetable_generator.room_capacity,
        timetable_generator.section_strength,
        timetable_generator.subject_quota_limits,
        timetable_generator.teacher_availability_preferences,
        timetable_generator.weekly_workload,
        Defaults.working_days
    )

    overall_fitness, fitness_scores = fitness_calculator.evaluate_timetable_fitness()


    # Selection of all Chromosomes
    selection_object = TimeTableSelection()
    print(selection_object.select_chromosomes(fitness_scores))


    # Crossover for all selected Chromosomes


    # Mutate all crossover Chromosomes


    # Store best of Chromosomes
run_timetable_generation()