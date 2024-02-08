import logging
from flask import request, jsonify
from backend.handlers.database import DatabaseHandler
from backend.utils.error import error_response
from backend.utils.token import token_required
from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/search', methods=['GET'])
def search_users():
    try:
        search_query = request.args.get('query')
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute(
            "SELECT u.id, u.username, u.profile_pic_url, COUNT(f1.follower_id) AS followers_count, COUNT(f2.followed_id) AS following_count, u.made_tasks, u.points, u.verified, u.description FROM users u LEFT JOIN follows f1 ON u.id = f1.followed_id LEFT JOIN follows f2 ON u.id = f2.follower_id WHERE u.username LIKE %s GROUP BY u.id",
            ('%' + search_query + '%',)
        )
        search_results = cursor.fetchall()

        db.close_connection()

        results_json = [{
            'id': result[0],
            'username': result[1],
            'profile_pic_url': result[2],
            'followers_count': result[3],
            'following_count': result[4],
            'made_tasks': result[5],
            'points': result[6],
            'verified': result[7],
            'description': result[8]
        } for result in search_results]

        return jsonify(results_json)
    except Exception as e:
        logging.error(f"Error searching users: {str(e)}")
        return error_response('Error searching users', 500)

@users_bp.route('/user/<string:identifier>', methods=['GET'])
@token_required
def user_profile(identifier):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        if request.args.get('fromid') == 'true':
            cursor.execute(
                "SELECT u.id, u.username, u.profile_pic_url, COUNT(f1.follower_id) AS followers_count, COUNT(f2.followed_id) AS following_count, u.made_tasks, u.points, u.verified, u.description FROM users u LEFT JOIN follows f1 ON u.id = f1.followed_id LEFT JOIN follows f2 ON u.id = f2.follower_id WHERE u.id = %s GROUP BY u.id",
                (identifier,)
            )
        elif request.args.get('fromid') == 'false':
            cursor.execute(
                "SELECT u.id, u.username, u.profile_pic_url, COUNT(f1.follower_id) AS followers_count, COUNT(f2.followed_id) AS following_count, u.made_tasks, u.points, u.verified, u.description FROM users u LEFT JOIN follows f1 ON u.id = f1.followed_id LEFT JOIN follows f2 ON u.id = f2.follower_id WHERE u.username = %s GROUP BY u.id",
                (identifier,)
            )

        user_data = cursor.fetchone()

        if not user_data:
            db.close_connection()
            return error_response('User not found', 404)

        user_profile_data = {
            'id': user_data[0],
            'username': user_data[1],
            'profile_pic_url': user_data[2],
            'followers_count': user_data[3],
            'following_count': user_data[4],
            'made_tasks': user_data[5],
            'points': user_data[6],
            'verified': user_data[7],
            'description': user_data[8]
        }

        db.close_connection()
        return jsonify(user_profile_data)
    except Exception as e:
        logging.error(f"Error fetching user profile: {str(e)}")
        return error_response('Failed to fetch user profile', 500)