from datetime import datetime

from Constants.constant import Defaults
from Constants.helper_routines import initialize_teacher_availability
from Samples.samples import TeacherWorkload, SpecialSubjects, SubjectWeeklyQuota
from GA.__init__ import run_timetable_generation
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mainapp.logics.teachers import TimetableSerializer
from ..drivers.mongo import MongoDriver
from ..drivers.postgres import PostgresDriver

import json

from Constants.is_conflict import IsConflict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from mainapp.converter.converter import csv_to_json


mongo_driver = MongoDriver()
pg_driver = PostgresDriver()

def generate_timetable_from_ga(
    lab_availability_matrix: dict,
    teacher_availability_matrix: dict,
    course_id: int,
    semester: int,
    teacher_subject_mapping: dict,
    total_sections: dict,
    total_classrooms: dict,
    total_labs: dict,
    teacher_preferences: dict,
    teacher_weekly_workload: dict,
    special_subjects: dict,
    labs: dict,
    subject_quota_limits: dict,
    teacher_duty_days: dict,
    total_generations: int,
    time_slots: dict,
    day_map: dict,
    time_slot_map: dict
):
    timetable, correct_teacher_availability_matrix, correct_lab_availability_matrix = run_timetable_generation(
        teacher_subject_mapping=teacher_subject_mapping,
        total_sections=total_sections,
        total_classrooms=total_classrooms,
        total_labs=total_labs,
        teacher_preferences=teacher_preferences,
        teacher_weekly_workload=teacher_weekly_workload,
        special_subjects=special_subjects,
        labs=labs,
        subject_quota_limits=subject_quota_limits,
        teacher_duty_days=teacher_duty_days,
        teacher_availability_matrix=teacher_availability_matrix,
        lab_availability_matrix=lab_availability_matrix,
        total_generations=total_generations,
        time_slots=time_slots,
        day_map=day_map,
        time_slot_map=time_slot_map
    )

    old_current_timetable = mongo_driver.find_one(
        "current_timetable",
        {"course_id": course_id, "semester": semester}
    )

    if old_current_timetable:
        mongo_driver.insert_one(
            collection_name="historical_timetable",
            document=old_current_timetable
        )
        mongo_driver.delete_one(
            collection_name="current_timetable",
            query={"course_id": course_id, "semester": semester}
        )

    new_doc = {
        "course_id": course_id,
        "semester": semester,
        "timetable": timetable,
        "last_updated": datetime.now().isoformat()
    }
    mongo_driver.insert_one(
        collection_name="current_timetable",
        document=new_doc
    )

    return timetable, correct_teacher_availability_matrix, correct_lab_availability_matrix


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_timetable(request):
    try:
        data = request.data
        course_id = data.get("course_id")
        semester = data.get("semester")
        department = data.get("department")

        if not course_id or not semester or not department:
            return Response({
                "error": "course_id, semester and department are required."},
                status=400
            )

        lab_doc = mongo_driver.find_one(
            "lab_availability_matrix",
            {}
        )

        if lab_doc:
            lab_availability_matrix = lab_doc.get("matrix")
        else:
            lab_availability_matrix = {
                "L1": [[True] * 7 for _ in range(5)],
                "L2": [[True] * 7 for _ in range(5)],
                "L3": [[True] * 7 for _ in range(5)],
                "L4": [[True] * 7 for _ in range(5)],
                "L5": [[True] * 7 for _ in range(5)],
                "L6": [[True] * 7 for _ in range(5)]
            }

            mongo_driver.insert_one("lab_availability_matrix", {
                "matrix": lab_availability_matrix
            })

        teacher_doc = mongo_driver.find_one(
            "teacher_availability_matrix",
            {
                "department_name": department
            }
        )

        if teacher_doc:
            teacher_availability_matrix = teacher_doc.get("matrix")

        else:
            teacher_ids = list(TeacherWorkload.Weekly_workLoad.keys())
            teacher_availability_matrix = initialize_teacher_availability(teacher_ids, 5, 7)
            mongo_driver.insert_one("teacher_availability_matrix", {
                "department_name": department,
                "matrix": teacher_availability_matrix
            })

        query = "SELECT subject_teacher_map FROM mainapp_teachersubject;"
        result = pg_driver.execute_query(query)

        if result:
            subject_teacher_map_str = str(result[0][0])
            valid_json_str = subject_teacher_map_str.replace("'", '"')
            teacher_subject_mapping = json.loads(valid_json_str)

        else:
            return Response({
                    "error": "Teacher subject mapping not found in Postgres."
                },
                status=400
            )

        timetable, updated_teacher_availability_matrix, updated_lab_availability_matrix = generate_timetable_from_ga(
            lab_availability_matrix=lab_availability_matrix,
            teacher_availability_matrix=teacher_availability_matrix,
            course_id=course_id,
            semester=semester,
            teacher_subject_mapping=teacher_subject_mapping,
            total_sections={"A": 70, "B": 100, "C": 75, "D": 100},
            total_classrooms={"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250},
            total_labs={"L1": 70, "L2": 50, "L3": 70, "L4": 50, "L5": 70, "L6": 50},
            teacher_preferences=TeacherWorkload.teacher_preferences,
            teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
            special_subjects=SpecialSubjects.special_subjects,
            labs=SpecialSubjects.Labs,
            subject_quota_limits=SubjectWeeklyQuota.subject_quota,
            teacher_duty_days=TeacherWorkload.teacher_duty_days,
            total_generations=Defaults.total_no_of_generations,
            time_slots={
                1: "9:00 - 9:55",
                2: "9:55 - 10:50",
                3: "11:10 - 12:05",
                4: "12:05 - 1:00",
                5: "1:20 - 2:15",
                6: "2:15 - 3:10",
                7: "3:30 - 4:25",
            },
            day_map={
                "Monday": 0,
                "Tuesday": 1,
                "Wednesday": 2,
                "Thursday": 3,
                "Friday": 4,
                "Saturday": 5,
                "Sunday": 6
            },
            time_slot_map={
                "9:00 - 9:55": 1,
                "9:55 - 10:50": 2,
                "11:10 - 12:05": 3,
                "12:05 - 1:00": 4,
                "1:20 - 2:15": 5,
                "2:15 - 3:10": 6,
                "3:30 - 4:25": 7
            }
        )

        mongo_driver.update_one(
            "lab_availability_matrix",
            {},
            {"$set": {"matrix": updated_lab_availability_matrix}}
        )
        mongo_driver.update_one(
            "teacher_availability_matrix",
            {"department_name": department},
            {"$set": {"matrix": updated_teacher_availability_matrix}}
        )

        return Response(
            timetable,
            status=200
        )

    except Exception as e:
        return Response({"error": f"Failed to generate timetable: {str(e)}"}, status=500)


@api_view(['POST'])
def update_time_table(request):
    """
        Replace the current timetable and archive the old version.
    """

    # Validate incoming data
    serializer = TimetableSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    course_id = data["course_id"]
    semester = data["semester"]
    timetable = data["timetable"]
    chromosome = data["chromosome"]

    current_collection = "current_timetable"
    historical_collection = "historical_timetable"

    # Define a query for the specific timetable
    query = {"course_id": course_id, "semester": semester}

    # Fetch the current timetable
    current_timetable = list(mongo_driver.find(current_collection, query))

    # If exists, move current timetable to historical and delete it from current_timetable
    if current_timetable:
        current_timetable = current_timetable[0]  # Assuming one timetable per course/semester
        historical_entry = {
            **current_timetable,
            "updated_at": datetime.utcnow().isoformat()  # Add timestamp
        }
        del historical_entry["_id"]  # Remove MongoDB ID for insertion
        mongo_driver.insert_one(historical_collection, historical_entry)
        mongo_driver.delete_one(current_collection, query)  # Remove old timetable

    # Insert the new timetable
    new_timetable_entry = {
        "course_id": course_id,
        "semester": semester,
        "timetable": timetable,
        "chromosome": chromosome,
        "last_updated": datetime.now().isoformat()  # Add last updated timestamp
    }
    mongo_driver.insert_one(
        current_collection,
        new_timetable_entry
    )

    return JsonResponse({"message": "Timetable updated successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_current_time_table(request, course_id, semester):
    """
    Fetch the current timetable for a given course and semester.
    """
    query = {"course_id": course_id, "semester": semester}
    current_timetable = list(mongo_driver.find("current_timetable", query))

    if not current_timetable:
        return JsonResponse({"error": "Current timetable not found"}, status=status.HTTP_404_NOT_FOUND)

    # Convert ObjectId to string in the current timetable
    for timetable in current_timetable:
        timetable["_id"] = str(timetable["_id"])  # Convert ObjectId to string

    return JsonResponse(current_timetable[0], safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_historical_time_table(request, course_id, semester):
    """
    Fetch the historical timetables for a given course and semester.
    """
    query = {"course_id": course_id, "semester": semester}
    historical_timetables = list(mongo_driver.find("historical_timetable", query))

    if not historical_timetables:
        return JsonResponse({"error": "No historical timetables found"}, status=status.HTTP_404_NOT_FOUND)

    for timetable in historical_timetables:
        timetable["_id"] = str(timetable["_id"])  # Convert ObjectId to string

    return JsonResponse(historical_timetables, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def detect_conflicts(request):
    if request.method == "POST" and request.FILES.getlist("csv_files"):
        try:
            csv_files = request.FILES.getlist("csv_files")
            timetables = []
            file_names = []

            for csv_file in csv_files:
                timetable_json = csv_to_json(csv_file)
                timetables.append(json.loads(timetable_json))
                file_names.append(csv_file.name)

            conflict_checker = IsConflict()
            conflict_results = []
            has_conflicts = False

            for i in range(len(timetables)):
                for j in range(i + 1, len(timetables)):
                    timetable1 = timetables[i]
                    timetable2 = timetables[j]

                    conflicts = conflict_checker.process_schedules(
                        timetable1, timetable2
                    )

                    if conflicts:
                        has_conflicts = True
                        conflict_results.append(
                            {
                                "timetable_1": file_names[i],
                                "timetable_2": file_names[j],
                                "conflict_details": conflicts,
                            }
                        )

            if has_conflicts:
                return JsonResponse({"conflicts": conflict_results}, status=200)
            else:
                return JsonResponse(
                    {"message": "No conflicts found between any two timetables."},
                    status=200,
                )

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse(
        {"error": "Invalid request. Please provide CSV files."}, status=400
    )

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def manual_timetable_upload(request):
    return Response({"ping": "pong"})
    # todo: I can have a clash in teacher, and classroom. Check that as well.

    # todo: Might people want to upload a single timetable.
    # todo: or multiple timetables.

    # todo: multiple department / single department.

    # todo: convert csv -> json (all / single TT)

    # todo: get the current timetable that are getting replaced, and also the teacher_availability_matrix + labs_availability_matrix

    # todo: is_confict check, on (upcoming TT / old non disturbed TT)

    # todo: create new matrix for labs + teachers, and save it to DB, also the historic table push is required.

    # todo: return success on successful change, or whatever exact error that file have.
    pass
