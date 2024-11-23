import psycopg2
import os

class PostgresDriver:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            self.connection.commit()

    def close(self):
        self.connection.close()
