from flask import request, jsonify
import bcrypt
import logging
import jwt
from backend.handlers.database import DatabaseHandler
from backend.config import SECRET_KEY
from backend.utils.error import error_response
from flask import Blueprint
from backend.utils.token import token_required

auth_bp = Blueprint('auth', __name__)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return error_response('Missing username, email, or password', 400)

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Store the user information in the database
        db = DatabaseHandler()
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))

        db.connection.commit()

        # After successfully registering, get the ID of the newly registered user
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()[0]

        # Generate a token JWT for the registered user
        payload = {'user_id': user_id}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        db.close_connection()

        # Return the token in the response along with a success message
        return jsonify(message='User registered successfully and logged in', token=token)
    except Exception as e:
        logging.error(f"Error registering user: {str(e)}")
        return error_response('User registration failed', 400)

# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return error_response('Missing email or password', 400)

        # Retrieve the user's stored hashed password from the database
        db = DatabaseHandler()
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            # After verifying the credentials and obtaining the user ID
            # Generate a token JWT for the authenticated user
            payload = {'user_id': user[0]}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            db.close_connection()

            return jsonify(message='Login successful', token=token)
        else:
            return error_response('Invalid credentials', 401)
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return error_response('Login failed', 500)