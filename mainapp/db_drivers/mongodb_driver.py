from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidURI
import os
from urllib.parse import quote_plus


class MongoDriver:
    def __init__(self):
        try:
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            db_name = os.getenv("MONGO_DB_NAME")
            uri_template = os.getenv("MONGO_DB_URI_TEMPLATE")

            encoded_username = quote_plus(username)
            encoded_password = quote_plus(password)

            self.mongo_uri = uri_template.format(
                username=encoded_username,
                password=encoded_password,
                dbname=db_name
            )

            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[db_name]

            # Test connection
            self.client.admin.command("ping")
            print("MongoDB connection established successfully.")

        except (ConnectionFailure, InvalidURI) as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name):
        # Get a MongoDB collection by name.
        return self.db[collection_name]

    def insert_one(self, collection_name, document):
        # Insert a single document into the specified collection.
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find(self, collection_name, query):
        # Query documents from the specified collection.
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def update_one(self, collection_name, query, update):
        # Update a single document in the specified collection.
        collection = self.get_collection(collection_name)
        return collection.update_one(query, update)

    def delete_one(self, collection_name, query):
        # Delete a single document from the specified collection.
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def list_collections(self):
        # List all collections in the connected database.
        return self.db.list_collection_names()
