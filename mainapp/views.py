from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver
from .models import Room, Teacher
from .serializers import RoomSerializer, TeacherSerializer
import os


def generateTimetable():
    pass


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
    Add a new room.
    """
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        generateTimetable()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


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
            generateTimetable()
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
        generateTimetable()
        return Response({"message": "Room deleted successfully"}, status=200)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)


@api_view(["GET"])
def getTeachers(request):
    """
    Retrieve a list of all teachers.
    """
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def addTeacher(request):
    """
    Add a new teacher.
    """
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        generateTimetable()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(["PUT"])
def updateTeacher(request, pk):
    """
    Update an existing teacher's detail by ID.
    """
    try:
        teacher = Teacher.objects.get(id=pk)
        serializer = TeacherSerializer(
            instance=teacher, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            generateTimetable()
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
        generateTimetable()
        return Response({"message": "Teacher deleted successfully"}, status=200)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)
