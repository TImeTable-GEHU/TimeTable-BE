from rest_framework.response import Response
from ..db_drivers.mongodb_driver import MongoDriver
from rest_framework.decorators import api_view
import json

mongo_driver = MongoDriver()

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

def save_chromosome(course_name, branch_name, semester_name, chromosome, mongo_driver):
        query = {"course.name": course_name}
        course_cursor = mongo_driver.find("currentTimeTable", query)

        # Fetch the first document (if any) or initialize it to None
        course_document = next(course_cursor, None)

        if not course_document:
            # Create a new course with branch and semester
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
            # Existing course found, update or add branch/semester
            updated = False

            for course_entry in course_document["course"]:
                if course_entry["name"] == course_name:
                    for branch in course_entry["branches"]:
                        if branch["name"] == branch_name:
                            for semester in branch["semesters"]:
                                if semester["name"] == semester_name:
                                    # Update existing semester
                                    semester["chromosome"] = chromosome
                                    updated = True
                                    break
                            if not updated:
                                # Add new semester
                                branch["semesters"].append({"name": semester_name, "chromosome": chromosome})
                                updated = True
                            break
                    if not updated:
                        # Add new branch
                        course_entry["branches"].append({
                            "name": branch_name,
                            "semesters": [{"name": semester_name, "chromosome": chromosome}]
                        })
                        updated = True
                    break

            if updated:
                mongo_driver.update_one(
                    "currentTimeTable", query, {"$set": {"course": course_document["course"]}}
                )
                print(f"Chromosome updated for course '{course_name}', branch '{branch_name}', semester '{semester_name}'.")
            else:
                print(f"Failed to update chromosome for course '{course_name}'.")

save_chromosome(
    course_name="Computer Science",
    branch_name="AI",
    semester_name="sem1",
    chromosome={"gene": [1, 0, 1, 1], "fitness": 0.95},
    mongo_driver=mongo_driver
)

# Save or update another chromosome
save_chromosome(
    course_name="Computer Science",
    branch_name="AI",
    semester_name="sem2",
    chromosome={"gene": [0, 1, 0, 1], "fitness": 0.85},
    mongo_driver=mongo_driver
)

# Save a new course
save_chromosome(
    course_name="Electronics",
    branch_name="VLSI",
    semester_name="sem1",
    chromosome={"gene": [1, 1, 1, 0], "fitness": 0.90},
    mongo_driver=mongo_driver
)
