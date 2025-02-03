# views.py
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from ..drivers.mongodb_driver import MongoDriver
from .serializers import TimetableSerializer
from django.http import JsonResponse

# Initialize MongoDB driver
mongo_driver = MongoDriver()

@api_view(['POST'])
def updateTimeTable(request):
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

    # Define query for the specific timetable
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
        "last_updated": datetime.utcnow().isoformat()  # Add last updated timestamp
    }
    mongo_driver.insert_one(current_collection, new_timetable_entry)

    return JsonResponse({"message": "Timetable updated successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getCurrentTimeTable(request, course_id, semester):
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
def getHistoricalTimeTable(request, course_id, semester):
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
