from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver
from .models import Room, Teacher, Subject, TeacherSubject, Student
from .serializers import RoomSerializer, TeacherSerializer, SubjectSerializer
import os


@api_view(["POST"])
def generate_timetable(request):
    """
    Generate a timetable using the provided data.
    """
    try:
        # generateTimetable()
        return Response({"message": "Timetable generated successfully"}, status=200)
    except Exception as e:
        return Response(
            {"error": f"Failed to generate timetable: {str(e)}"}, status=500
        )


@api_view(["GET"])
def mongo_status(request):
    """
    Check MongoDB connection status.
    """
    try:
        mongo_driver = MongoDriver()
        collections = mongo_driver.db.list_collection_names()
        return JsonResponse({"mongodb": "Connected", "collections": collections})
    except Exception as e:
        return JsonResponse({"mongodb": "Not Connected", "error": str(e)})


@api_view(["GET"])
def postgres_status(request):
    """
    Check PostgreSQL connection status.
    """
    try:
        postgres_driver = PostgresDriver(
            dbname=os.getenv("POSTGRES_NAME"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
            options="-c search_path=public",
            logger=None,
        )
        query = "SELECT 1;"  # Simple query to validate the connection
        result = postgres_driver.execute_query(query)
        return JsonResponse({"postgresql": "Connected", "result": result})
    except Exception as e:
        return JsonResponse({"postgresql": "Not Connected", "error": str(e)})


@api_view(["GET"])
def getRooms(request):
    """
    Retrieve a list of all rooms.
    """
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def addRoom(request):
    """
    Add one or multiple rooms.
    """
    data = request.data if isinstance(request.data, list) else [request.data]
    added_rooms = []
    errors = []

    for room_data in data:
        serializer = RoomSerializer(data=room_data)
        if serializer.is_valid():
            serializer.save()
            added_rooms.append(serializer.data)
        else:
            errors.append({"room_data": room_data, "errors": serializer.errors})

    if errors:
        return Response(
            {"added_rooms": added_rooms, "errors": errors},
            status=400 if not added_rooms else 207,
        )
    return Response(added_rooms, status=201)


@api_view(["PUT"])
def updateRoom(request, pk):
    """
    Update an existing room by ID.
    """
    try:
        room = Room.objects.get(id=pk)
        serializer = RoomSerializer(instance=room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)


@api_view(["DELETE"])
def deleteRoom(request, pk):
    """
    Delete a room by ID.
    """
    try:
        room = Room.objects.get(id=pk)
        room.delete()
        return Response({"message": "Room deleted successfully"}, status=200)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)


@api_view(["GET"])
def getTeachers(request):
    """
    Retrieve a list of all teachers along with their preferred subjects.
    """
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def addTeacher(request):
    """
    Add a new teacher and map the preferred subjects to the teacher.
    """
    serializer = TeacherSerializer(data=request.data["teacher"])

    if serializer.is_valid():
        teacher = serializer.save()
        preferred_subjects = request.data.get("preferred_subjects", [])

        subjects = Subject.objects.filter(subject_name__in=preferred_subjects)

        for subject in subjects:
            TeacherSubject.objects.create(teacher_id=teacher, subject_id=subject)

        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(["PUT"])
def updateTeacher(request, pk):
    """
    Update an existing teacher's detail by ID, including preferred subjects.
    """
    try:
        teacher = Teacher.objects.get(id=pk)
        serializer = TeacherSerializer(
            instance=teacher, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            if "preferred_subjects" in request.data:
                preferred_subjects = request.data["preferred_subjects"]
                # Clear existing preferred subjects
                TeacherSubject.objects.filter(teacher_id=teacher).delete()
                # Map the teacher to the new preferred subjects
                for subject_name in preferred_subjects:
                    try:
                        subject = Subject.objects.get(subject_name=subject_name)
                        TeacherSubject.objects.create(
                            teacher_id=teacher, subject_id=subject
                        )
                    except Subject.DoesNotExist:
                        return Response(
                            {"error": f"Subject '{subject_name}' not found"}, status=404
                        )

            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)


@api_view(["DELETE"])
def deleteTeacher(request, pk):
    """
    Delete a teacher by ID.
    """
    try:
        teacher = Teacher.objects.get(id=pk)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully"}, status=200)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)


@api_view(["GET"])
def getAllSubjects(request):
    """
    Retrieve a list of all subjects.
    """
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def getFilteredSubjects(request):
    """
    Retrieve subjects based on department, course, branch, and semester.
    """
    dept = request.GET.get("dept")
    course = request.GET.get("course")
    branch = request.GET.get("branch", "")  # Default to an empty string
    semester = request.GET.get("semester")

    if not all([dept, course, semester]):
        return Response(
            {"error": "Please provide dept, course, and semester."},
            status=400,
        )

    filters = {
        "dept": dept,
        "course": course,
        "semester": semester,
    }
    if branch:  # Add branch to filters only if it's provided
        filters["branch"] = branch

    subjects = Subject.objects.filter(**filters)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def addSubject(request):
    """
    Add one or multiple subjects to a specific dept, course, branch, and semester.
    """
    if isinstance(request.data, list):
        subjects_data = request.data
    else:
        subjects_data = [request.data]

    errors = []

    for subject_data in subjects_data:
        dept = subject_data.get("dept")
        course = subject_data.get("course")
        branch = subject_data.get("branch", "")
        semester = subject_data.get("semester")

        if not all([dept, course, semester]):
            errors.append(
                {"error": "Please provide dept, course, and semester for each subject."}
            )
            continue

        subject_name = subject_data.get("subject_name")
        subject_code = subject_data.get("subject_code")
        credits = subject_data.get("credits")

        if not all([subject_name, subject_code, credits]):
            errors.append(
                {
                    "error": "Please provide subject_name, subject_code, and credits for each subject."
                }
            )
            continue

        subject_dict = {
            "subject_name": subject_name,
            "subject_code": subject_code,
            "credits": credits,
            "dept": dept,
            "course": course,
            "branch": branch,
            "semester": semester,
        }

        serializer = SubjectSerializer(data=subject_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            errors.append(serializer.errors)

    if errors:
        return Response(errors, status=400)

    return Response({"message": "Subjects added successfully."}, status=201)


@api_view(["PUT"])
def updateSubject(request, pk):
    """
    Update an existing subject by ID.
    """
    try:
        subject = Subject.objects.get(id=pk)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=404)

    serializer = SubjectSerializer(instance=subject, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def deleteSubject(request, pk):
    """
    Delete a subject by ID.
    """
    try:
        subject = Subject.objects.get(id=pk)
        subject.delete()
        return Response({"message": "Subject deleted successfully"}, status=200)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=404)


def addStudent(
    student_name,
    student_id,
    is_hosteller,
    location,
    dept,
    course,
    branch,
    semester,
    section,
    cgpa,
):
    try:
        student = Student.objects.create(
            student_name=student_name,
            student_id=student_id,
            is_hosteller=is_hosteller,
            location=location,
            dept=dept,
            course=course,
            branch=branch,
            semester=semester,
            section=section,
            cgpa=cgpa,
        )
        return {
            "status": "success",
            "message": "Student added successfully",
            "student": student,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
