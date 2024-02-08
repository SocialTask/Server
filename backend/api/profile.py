import os
import logging
from flask import request, jsonify, g
from flask import Blueprint
from backend.handlers.database import DatabaseHandler
from backend.utils.error import error_response
from backend.utils.token import token_required
from PIL import Image
import backend.config
import time

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/upload-picture', methods=['POST'])
@token_required
def upload_picture():
    try:
        user_id = g.user_id

        if 'file' not in request.files:
            return error_response('No file part', 400)

        file = request.files['file']

        if file.filename == '':
            return error_response('No selected file', 400)

        file_type = request.form.get('file_type')

        if file_type not in ('profile_picture', 'cover_photo'):
            return error_response('Invalid file type', 400)

        # Construct the upload folder path
        upload_folder = 'backend/storage/profile_pictures/' if file_type == 'profile_picture' else 'backend/storage/profile_covers/'

        unique_filename = f'user_{user_id}_{int(time.time())}.jpg'

        file_path = os.path.join(upload_folder, unique_filename)
        print(file_path)
        file.save(file_path)

        if file_type == 'profile_picture':
            compress_profile_image(file_path)

        # Construct the image URL
        base_url = backend.config.BASE_URL
        image_path = upload_folder.split("backend")[-1]
        image_url = f"{base_url}{image_path}{unique_filename}"

        db = DatabaseHandler()
        cursor = db.connection.cursor()
        cursor.execute("UPDATE users SET profile_pic_url = %s WHERE id = %s", (image_url, user_id))
        db.connection.commit()
        db.close_connection()

        return jsonify(file_url=image_url)

    except Exception as e:
        error_message = f'Error while uploading file: {str(e)}'
        logging.error(error_message)
        return error_response(error_message, 500)

def compress_profile_image(file_path):
    try:
        img = Image.open(file_path)
        img = img.convert("RGB")
        img.thumbnail((300, 300))
        img.save(file_path, 'JPEG', quality=50)
    except Exception as e:
        logging.error(f'Error while compressing profile image: {str(e)}')

@profile_bp.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile():
    if request.method == 'GET':
        try:
            db = DatabaseHandler()
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.profile_pic_url, u.privacy_setting, u.made_tasks, u.points, u.verified, u.description, u.cover_photo_url,
                COUNT(f1.follower_id) AS followers_count, COUNT(f2.followed_id) AS following_count
                FROM users u
                LEFT JOIN follows f1 ON u.id = f1.followed_id
                LEFT JOIN follows f2 ON u.id = f2.follower_id
                WHERE u.id = %s
                GROUP BY u.id
                """, (g.user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                db.close_connection()
                return error_response('User not found', 404)

            profile_data = {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'profile_pic_url': user_data[3],
                'privacy_setting': user_data[4],
                'made_tasks': user_data[5],
                'points': user_data[6],
                'verified': user_data[7],
                'description': user_data[8],
                'cover_photo_url': user_data[9],
                'followers_count': user_data[10],
                'following_count': user_data[11],
            }

            db.close_connection()
            return jsonify(profile_data)
        except Exception as e:
            logging.error(f"Error fetching user profile: {str(e)}")
            return error_response('Failed to fetch user profile', 500)
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            profile_pic_url = data.get('profile_pic_url')
            cover_photo_url = data.get('cover_photo_url')
            privacy_setting = data.get('privacy_setting')
            description = data.get('description')

            db = DatabaseHandler()
            cursor = db.connection.cursor()

            new_profile_pic = upload_picture(request, 'profile_picture')
            if new_profile_pic:
                profile_pic_url = new_profile_pic

            new_cover_photo = upload_picture(request, 'cover_photo')
            if new_cover_photo:
                cover_photo_url = new_cover_photo

            cursor.execute("""
                UPDATE users SET profile_pic_url = %s, cover_photo_url = %s, privacy_setting = %s, description = %s WHERE id = %s
                """, (profile_pic_url, cover_photo_url, privacy_setting, description, g.user_id))
            db.connection.commit()

            db.close_connection()
            return jsonify(message='Profile updated successfully')
        except Exception as e:
            logging.error(f"Error updating user profile: {str(e)}")
            return error_response('Failed to update user profile', 500)
