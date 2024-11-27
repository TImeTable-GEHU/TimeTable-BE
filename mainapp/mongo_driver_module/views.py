from rest_framework.response import Response
from ..db_drivers.mongodb_driver import MongoDriver
from rest_framework.decorators import api_view
import json
from datetime import datetime
from bson import ObjectId

mongo_driver = MongoDriver()


def convert_objectid(document):
    if isinstance(document, list):
        return [convert_objectid(item) for item in document]
    elif isinstance(document, dict):
        return {key: convert_objectid(value) for key, value in document.items()}
    elif isinstance(document, ObjectId):
        return str(document)
    else:
        return document

@api_view(['GET'])
def getCurrentTimeTable(request):
    try:
        query = request.query_params.get("query", "{}")
        query = json.loads(query)
        documents = list(mongo_driver.find("currentTimeTable", query))
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return Response(documents, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def getHistoricalTimeTable(request):
    try:
        # Parse the query parameter
        query = request.query_params.get("query", "{}")
        query = json.loads(query)

        # Fetch documents from MongoDB
        documents = list(mongo_driver.find("historical_timetables", query))

        # Convert all ObjectId fields to strings
        documents = convert_objectid(documents)

        # Return the documents as a JSON response
        return Response(documents, status=200)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON in query parameter"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


def save_chromosome(course_name, branch_name, semester_name, chromosome, mongo_driver):
    # Query to find the course
    query = {"course.name": course_name}
    course_cursor = mongo_driver.find("currentTimeTable", query)
    course_document = next(course_cursor, None)

    if not course_document:
        # Create a new course structure if not exists
        new_course = {
            "course": [
                {
                    "name": course_name,
                    "branches": [
                        {
                            "name": branch_name,
                            "semesters": [
                                {"name": semester_name, "chromosome": chromosome}
                            ]
                        }
                    ]
                }
            ]
        }
        mongo_driver.insert_one("currentTimeTable", new_course)
        print(f"New course '{course_name}' with branch '{branch_name}' and semester '{semester_name}' added.")
    else:
        # Ensure branches and semesters exist before updating
        updated = False
        for course_entry in course_document["course"]:
            if course_entry["name"] == course_name:
                if "branches" not in course_entry:
                    course_entry["branches"] = []
                for branch in course_entry["branches"]:
                    if branch["name"] == branch_name:
                        if "semesters" not in branch:
                            branch["semesters"] = []
                        for semester in branch["semesters"]:
                            if semester["name"] == semester_name:
                                semester["chromosome"] = chromosome  # Update existing semester
                                updated = True
                                break
                        if not updated:
                            branch["semesters"].append({"name": semester_name, "chromosome": chromosome})
                            updated = True
                        break
                if not updated:
                    course_entry["branches"].append({
                        "name": branch_name,
                        "semesters": [{"name": semester_name, "chromosome": chromosome}]
                    })
                    updated = True
                break

        if updated:
            mongo_driver.update_one(
                "currentTimeTable",
                query,
                {"$set": {"course": course_document["course"]}}
            )
            print(f"Chromosome updated for course '{course_name}', branch '{branch_name}', semester '{semester_name}'.")
        else:
            print(f"Failed to update chromosome for course '{course_name}'.")


def archive_current_timetable(mongo_driver):
    current_timetables = list(mongo_driver.find("currentTimeTable", {}))  # Fetch all documents

    if not current_timetables:
        print("No current timetables found to archive.")
        return

    for document in current_timetables:
        document.pop("_id", None)

    historical_entry = {
        "timestamp": datetime.now().isoformat(),  # Add a timestamp for versioning
        "timetables": current_timetables
    }

    mongo_driver.insert_one("historical_timetables", historical_entry)
    print("Archived the current timetable state to historical timetables.")

    # Step 3: Optionally clear the current timetable collection
    mongo_driver.delete_many("currentTimeTable", {})  # Clear all documents
    print("Cleared the current timetable collection.")

if __name__=="__main__":
    save_chromosome(
        course_name="Computer Science",
        branch_name="AI",
        semester_name="sem1",
        chromosome={"gene": [1, 0, 1, 1], "fitness": 0.95},
        mongo_driver=mongo_driver
    )

    save_chromosome(
        course_name="Computer Science",
        branch_name="AI",
        semester_name="sem2",
        chromosome={"gene": [0, 1, 0, 1], "fitness": 0.85},
        mongo_driver=mongo_driver
    )

    save_chromosome(
        course_name="Electronics",
        branch_name="VLSI",
        semester_name="sem1",
        chromosome={"gene": [1, 1, 1, 0], "fitness": 0.90},
        mongo_driver=mongo_driver
    )
    archive_current_timetable(
        mongo_driver=mongo_driver
    )
