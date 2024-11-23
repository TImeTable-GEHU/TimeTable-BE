from django.http import JsonResponse
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


def generateTimetable():
    pass


def mongo_status(request):
    try:
        mongo_driver = MongoDriver()
        collections = mongo_driver.db.list_collection_names()
        return JsonResponse({"mongodb": "Connected", "collections": collections})
    except Exception as e:
        return JsonResponse({"mongodb": "Not Connected", "error": str(e)})


def postgres_status(request):
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
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def addRoom(request):
    serializer = RoomSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        generateTimetable()
        return Response(serializer.data, status=201)
    else:
        return Response(status=400)


@api_view(["PUT"])
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(instance=room, data=request.data)

    if serializer.is_valid():
        serializer.save()
        generateTimetable()
        return Response(serializer.data, status=200)

    else:
        return Response(status=400)


@api_view(["DELETE"])
def deleteRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
        room.delete()
        generateTimetable()
        return Response(status=200)
    except:
        return Response(status=400)
