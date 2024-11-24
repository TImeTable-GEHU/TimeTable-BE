from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver
from .models import Room
from .serializers import RoomSerializer
import os


def generateTimetable():
    pass


class MongoStatusView(APIView):
    """
    View for checking the connection status of MongoDB.
    If MongoDB is connected, it returns a list of collections in the database.
    """

    def get(self, request):
        try:
            mongo_driver = MongoDriver()
            collections = mongo_driver.db.list_collection_names()
            return JsonResponse({"mongodb": "Connected", "collections": collections})
        except Exception as e:
            return JsonResponse({"mongodb": "Not Connected", "error": str(e)})


class PostgresStatusView(APIView):
    """
    View for checking the connection status of PostgreSQL.
    If PostgreSQL is connected, it returns a simple query result.
    """

    def get(self, request):
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
            query = "SELECT 1;"
            result = postgres_driver.execute_query(query)
            return JsonResponse({"postgresql": "Connected", "result": result})
        except Exception as e:
            return JsonResponse({"postgresql": "Not Connected", "error": str(e)})


class RoomViewSet(APIView):
    """
    Viewset for managing rooms. Supports GET, POST, PUT, DELETE operations.
    """

    def get(self, request, pk=None):
        """
        Retrieve a list of rooms.
        """
        if pk:
            try:
                room = Room.objects.get(id=pk)
                serializer = RoomSerializer(room)
                return Response(serializer.data, status=200)
            except Room.DoesNotExist:
                return Response({"error": "Room not found"}, status=404)
        else:
            rooms = Room.objects.all()
            serializer = RoomSerializer(rooms, many=True)
            return Response(serializer.data, status=200)

    def post(self, request):
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

    def put(self, request, pk):
        """
        Update an existing room.
        """
        try:
            room = Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)

        serializer = RoomSerializer(instance=room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            generateTimetable()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """
        Delete a room.
        """
        try:
            room = Room.objects.get(id=pk)
            room.delete()
            generateTimetable()
            return Response({"message": "Room deleted successfully"}, status=200)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)
