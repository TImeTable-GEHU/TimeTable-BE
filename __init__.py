# This is the Orchestrator file, which will govern the flow.


from Constants.constant import Defaults
from GA.mutation import TimeTableMutation
from GA.selection import TimeTableSelection
from GA.fitness import TimetableFitnessEvaluator
from GA.chromosome import TimeTableGeneration
from Samples.samples import SubjectTeacherMap, TeacherWorkload, SpecialSubjects, SubjectWeeklyQuota, Classrooms


def timetable_generation():

    # Create Chromosomes
    timetable_generator = TimeTableGeneration(
            teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
            total_sections=6,
            total_classrooms=8,
            total_labs=3,
            teacher_preferences=TeacherWorkload.teacher_preferences,
            teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
            special_subjects=SpecialSubjects.special_subjects,
            subject_quota_limits=SubjectWeeklyQuota.subject_quota,
            labs_list=Classrooms.labs,
        )

    timetable = timetable_generator.create_timetable(Defaults.initial_no_of_chromosomes)
    print(timetable)

    # Fitness of each Chromosome
    fitness_calculator = TimetableFitnessEvaluator(
            timetable,
            timetable_generator.sections,
            SubjectTeacherMap.subject_teacher_map,
            timetable_generator.classrooms,
            timetable_generator.lab_classrooms,
            timetable_generator.room_capacity,
            timetable_generator.section_strength,
            SubjectWeeklyQuota.subject_quota,
            timetable_generator.teacher_availability_preferences,
            timetable_generator.weekly_workload,
            Defaults.working_days
        )

    fitness_scores = fitness_calculator.evaluate_timetable_fitness()
    print(fitness_scores)


    # Selection of all Chromosomes
    selection_object = TimeTableSelection()
    from icecream import ic
    ic(fitness_scores)
    ic(selection_object.select_chromosomes(fitness_scores[0]))


    # Crossover for all selected Chromosomes
    # timetable_mutation_object = TimeTableMutation()
    # timetable_mutation_object.mutate_schedule_for_week()


    # Mutate all crossover Chromosomes


    # Store best of Chromosomes


def run_timetable_generation():
    for generation in range(Defaults.total_no_of_generations):
        # todo: refactor this to support next generations.
        timetable_generation()

timetable_generation()
