import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self, host='localhost', database='project_management', user='root', password='2468'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print(f"Connected to the database {self.database}")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error: {e}")

    def fetch_all(self, query, params=None):
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
