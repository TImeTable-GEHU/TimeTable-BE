from django.http import JsonResponse
from .db_drivers.mongodb_driver import MongoDriver
from .db_drivers.postgres_driver import PostgresDriver
import os


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
