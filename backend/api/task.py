import logging
import schedule
from flask import request, jsonify, g
from backend.handlers.database import DatabaseHandler
from backend.utils.error import error_response
from backend.utils.token import token_required
from flask import Blueprint

task_bp = Blueprint('task', __name__)

# Schedule function to update the selected task ID
selected_task_id = None

def update_random_task():
    try:
        # Connect to the database and retrieve a random task ID
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute("SELECT TaskID FROM tasks WHERE Status <> 0 ORDER BY RAND() LIMIT 1")
        task_id = cursor.fetchone()

        db.close_connection()

        if task_id:
            global selected_task_id
            selected_task_id = task_id[0]
    except Exception as e:
        logging.error(f"Error updating random task ID: {str(e)}")

# Schedule the task update to run every day at 10 AM server time
schedule.every().day.at("10:00").do(update_random_task)

# Endpoint to retrieve the selected task details
@task_bp.route('/task', methods=['GET'])
@token_required
def get_selected_task():
    global selected_task_id
    if selected_task_id is not None:
        try:
            # Connect to the database and retrieve the task details using the stored task ID
            db = DatabaseHandler()
            cursor = db.connection.cursor()

            cursor.execute("SELECT Name, Description, Category, Explanation, Feature1, Feature2, Feature3 FROM tasks WHERE TaskID = %s", (selected_task_id,))
            task_data = cursor.fetchone()

            db.close_connection()

            if task_data:
                task = {
                    'TaskID': selected_task_id,
                    'Name': task_data[0],
                    'Description': task_data[1],
                    'Category': task_data[2],
                    'Explanation': task_data[3],
                    'Feature1': task_data[4],
                    'Feature2': task_data[5],
                    'Feature3': task_data[6],
                }
                return jsonify(task)
            else:
                return error_response('Task details not found', 404)
        except Exception as e:
            logging.error(f"Error retrieving task details: {str(e)}")
            return error_response('Failed to retrieve task details', 500)
    else:
        return error_response('No task available', 404)
