import logging
from flask import jsonify, g, Blueprint
from backend.handlers.database import DatabaseHandler
from backend.utils.error import error_response
from backend.utils.token import token_required

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/follow/<int:user_id_to_follow>', methods=['POST'])
@token_required
def follow_user(user_id_to_follow):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        # Check if the user to follow exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id_to_follow,))
        followed_user = cursor.fetchone()

        if not followed_user:
            db.close_connection()
            return error_response('User to follow not found', 404)

        # Check if the user is trying to follow themselves
        if user_id_to_follow == g.user_id:
            db.close_connection()
            return error_response('You cannot follow yourself', 400)

        # Check if the user is already following the target user
        cursor.execute("SELECT 1 FROM follows WHERE follower_id = %s AND followed_id = %s", (g.user_id, user_id_to_follow))
        existing_follow = cursor.fetchone()

        if existing_follow:
            db.close_connection()
            return error_response('You are already following this user', 400)

        # Insert the follow relationship into the database
        cursor.execute("INSERT INTO follows (follower_id, followed_id) VALUES (%s, %s)", (g.user_id, user_id_to_follow))
        db.connection.commit()
        db.close_connection()

        return jsonify(message='You are now following this user')
    except Exception as e:
        logging.error(f"Error following user: {str(e)}")
        return error_response('Failed to follow user', 500)

@follow_bp.route('/unfollow/<int:user_id_to_unfollow>', methods=['POST'])
@token_required
def unfollow_user(user_id_to_unfollow):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        # Check if the user to unfollow exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id_to_unfollow,))
        followed_user = cursor.fetchone()

        if not followed_user:
            db.close_connection()
            return error_response('User to unfollow not found', 404)

        # Check if the user is trying to unfollow themselves
        if user_id_to_unfollow == g.user_id:
            db.close_connection()
            return error_response('You cannot unfollow yourself', 400)

        # Check if the user is not following the target user
        cursor.execute("SELECT 1 FROM follows WHERE follower_id = %s AND followed_id = %s", (g.user_id, user_id_to_unfollow))
        existing_follow = cursor.fetchone()

        if not existing_follow:
            db.close_connection()
            return error_response('You are not following this user', 400)

        # Remove the follow relationship from the database
        cursor.execute("DELETE FROM follows WHERE follower_id = %s AND followed_id = %s", (g.user_id, user_id_to_unfollow))
        db.connection.commit()
        db.close_connection()

        return jsonify(message='You have unfollowed this user')
    except Exception as e:
        logging.error(f"Error unfollowing user: {str(e)}")
        return error_response('Failed to unfollow user', 500)

@follow_bp.route('/followStatus/<int:user_id_to_check>', methods=['GET'])
@token_required
def follow_status(user_id_to_check):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        # Check if the current user is following the specified user
        cursor.execute("SELECT 1 FROM follows WHERE follower_id = %s AND followed_id = %s", (g.user_id, user_id_to_check))
        is_following = cursor.fetchone() is not None

        db.close_connection()

        return jsonify({'isFollowing': is_following})
    except Exception as e:
        logging.error(f"Error checking follow status: {str(e)}")
        return error_response('Failed to check follow status', 500)
