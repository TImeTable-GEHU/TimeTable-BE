from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidURI
import os
from urllib.parse import quote_plus


class MongoDriver:
    def __init__(self):
        self.client = None
        self.db = None
        self.mongo_uri = None
        self._setup_connection()

    def _setup_connection(self):
        try:
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            db_name = os.getenv("MONGO_DB_NAME")
            uri_template = os.getenv("MONGO_DB_URI_TEMPLATE")

            if not username or not password or not db_name or not uri_template:
                raise ValueError("MongoDB credentials or URI template are missing in environment variables")

            encoded_username = quote_plus(username)
            encoded_password = quote_plus(password)

            self.mongo_uri = uri_template.format(
                username=encoded_username,
                password=encoded_password,
                dbname=db_name
            )

            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[db_name]

            self._test_connection()

        except (ConnectionFailure, InvalidURI) as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
        except ValueError as ve:
            raise ve

    def _test_connection(self):
        try:
            self.client.admin.command("ping")
            print("MongoDB connection established successfully.")
        except Exception as e:
            raise ConnectionError(f"MongoDB connection failed: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def delete_many(self, collection_name, filter):
            collection = self.db[collection_name]
            result = collection.delete_many(filter)
            return result.deleted_count

    def insert_one(self, collection_name, document):
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def update_one(self, collection_name, query, update, array_filters=None):
        collection = self.get_collection(collection_name)
        if array_filters:
            return collection.update_one(query, update, array_filters=array_filters)
        return collection.update_one(query, update)

    def delete_one(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def list_collections(self):
        return self.db.list_collection_names()

    def save_file(self, filename, file_data):
        file_id = self.fs.put(file_data, filename=filename, content_type="application/zip")
        return str(file_id)

    def get_file(self, file_id):
        return self.fs.get(file_id)

    def delete_file(self, file_id):
        self.fs.delete(file_id)
