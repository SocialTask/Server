import bcrypt
import logging
import jwt
import os
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS
from functools import wraps
from werkzeug.utils import secure_filename
from backend.handlers.database import DatabaseHandler
from backend.config import SECRET_KEY

from backend.utils.error import error_response

# Define a decorator to require a valid token for route access
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the token from the URL query parameter
        token = request.args.get('token')

        if not token:
            return error_response('Token is missing', 401)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return error_response('Token has expired', 401)
        except jwt.InvalidTokenError:
            return error_response('Invalid token', 401)

        return f(*args, **kwargs)

    return decorated_function