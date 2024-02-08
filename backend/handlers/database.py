import mysql.connector
import logging
from backend.config import DATABASE_CONFIG
from cachetools import cached, LRUCache
import threading
from queue import Queue

# Define a lock for controlling database access
db_lock = threading.Semaphore(1)  # Max 1 concurrent database connection

# Define a queue for holding requests beyond the limit
request_queue = Queue()

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            if self.connection.is_connected():
                logging.info("Connected to the database")
        except mysql.connector.Error as err:
            logging.error("Error connecting to the database: %s", err)

        # Define the cache
        self.cache = LRUCache(maxsize=100)

        # Assign the cached decorator to a class attribute
        self.cached_execute_query = cached(cache=lambda: self.cache)(self.execute_query)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")

    def execute_query(self, query, data=None):
        cursor = None
        try:
            db_lock.acquire()  # Acquire the lock
            cursor = self.connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except mysql.connector.Error as err:
            self.connection.rollback()
            logging.error("Error executing query: %s", err)
        finally:
            if cursor:
                cursor.close()
            db_lock.release()  # Release the lock

            # Check if there are requests in the queue, if so, process them
            if not request_queue.empty():
                request = request_queue.get()
                self.process_request(request)

    def process_request(self, request):
        query, data = request
        try:
            result = self.execute_query(query, data)
            # Process the result or handle it as needed
            print("Processed request:", result)
        except Exception as e:
            # Handle exceptions appropriately
            print("Error processing request:", e)

    def clear_cache(self):
        self.cache.clear()
