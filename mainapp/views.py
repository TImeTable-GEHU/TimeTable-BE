from django.http import JsonResponse
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver


def mongo_status(request):
    try:
        mongo_driver = MongoDriver()
        collections = mongo_driver.db.list_collection_names()
        return JsonResponse({
            "mongodb": "Connected",
            "collections": collections
        })
    except Exception as e:
        return JsonResponse({
            "mongodb": "Not Connected",
            "error": str(e)
        })


def postgres_status(request):
    try:
        postgres_driver = PostgresDriver()
        query = "SELECT 1;"  # Simple query to validate the connection
        result = postgres_driver.execute_query(query)
        return JsonResponse({
            "postgresql": "Connected",
            "result": result
        })
    except Exception as e:
        return JsonResponse({
            "postgresql": "Not Connected",
            "error": str(e)
        })
