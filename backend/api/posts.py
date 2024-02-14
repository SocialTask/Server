from flask import Blueprint, request, jsonify, g
import logging
import os
from datetime import datetime
from PIL import Image, ExifTags
from flask import current_app as app
from flask_cors import CORS
from backend.handlers.database import DatabaseHandler
from backend.utils.token import token_required
from backend.utils.error import error_response
from werkzeug.utils import secure_filename
import backend.config
import random
import string
import cv2

# Define a list of allowed image file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'}

# Create a Blueprint for the posts API
posts_bp = Blueprint('posts', __name__)

# Function to check if a filename has an allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts_bp.route('/post', methods=['POST'])
@token_required
def create_post():
    try:
        text = request.form.get('text', '')
        media_file = request.files.get('media')

        raw_media_url = None
        compressed_media_url = None
        video_url = None

        if media_file and allowed_file(media_file.filename):
            if any(media_file.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                print("Image")
                # Procesar imagen
                unique_filename = generate_unique_filename(media_file.filename)
                raw_upload_folder = os.path.join('backend', 'storage', 'images', 'raw', datetime.now().strftime("%Y%m%d"))
                compressed_upload_folder = os.path.join('backend', 'storage', 'images', 'compressed', datetime.now().strftime("%Y%m%d"))
                os.makedirs(raw_upload_folder, exist_ok=True)
                os.makedirs(compressed_upload_folder, exist_ok=True)

                raw_temp_image_path = os.path.join(raw_upload_folder, unique_filename)
                media_file.save(raw_temp_image_path)

                with Image.open(raw_temp_image_path) as img:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    if img._getexif() is not None:
                        exif = dict(img._getexif().items())
                        if orientation in exif:
                            if exif[orientation] == 3:
                                img = img.rotate(180, expand=True)
                            elif exif[orientation] == 6:
                                img = img.rotate(270, expand=True)
                            elif exif[orientation] == 8:
                                img = img.rotate(90, expand=True)

                    img = img.convert("RGB")
                    img.thumbnail((1000, 1000))
                    compressed_temp_image_path = os.path.join(compressed_upload_folder, unique_filename)
                    img.save(compressed_temp_image_path, format="JPEG", quality=75)

                relative_raw_path = raw_temp_image_path.split("backend")[-1]
                relative_compressed_path = compressed_temp_image_path.split("backend")[-1]
                raw_media_url = f"{backend.config.BASE_URL}{relative_raw_path}"
                compressed_media_url = f"{backend.config.BASE_URL}{relative_compressed_path}"

            elif any(media_file.filename.lower().endswith(ext) for ext in ['.avi', '.mp4', '.mkv']):
                print("Video")
                # Procesar video
                unique_filename = generate_unique_filename(media_file.filename)
                video_upload_folder = os.path.join('backend', 'storage', 'videos', datetime.now().strftime("%Y%m%d"))
                os.makedirs(video_upload_folder, exist_ok=True)

                video_path = os.path.join(video_upload_folder, unique_filename)
                media_file.save(video_path)

                video_url = f"{backend.config.BASE_URL}{video_path.split('backend')[-1]}"

                                # Generar imagen de video
                video_thumbnail_path = generate_video_thumbnail(video_path)

                video_thumbnail = f"{backend.config.BASE_URL}{video_thumbnail_path.split('backend')[-1]}"

        db = DatabaseHandler()
        cursor = db.connection.cursor()
        
        if video_url:
            cursor.execute("INSERT INTO posts (user_id, text, video_url, video_thumbnail) VALUES (%s, %s, %s, %s)",
                        (g.user_id, text, video_url, video_thumbnail))
        else:
            cursor.execute("INSERT INTO posts (user_id, text, img_raw, img_compressed) VALUES (%s, %s, %s, %s)",
                        (g.user_id, text, raw_media_url, compressed_media_url))

        db.connection.commit()
        post_id = cursor.lastrowid

        db.close_connection()

        return jsonify(message='Post created successfully', post_id=post_id)
    except Exception as e:
        logging.error(f"Error creating post: {str(e)}")
        return error_response('Failed to create post', 500)

def generate_video_thumbnail(video_path):
    try:
        if not os.path.isfile(video_path):
            print("El archivo de video no existe.")
            return None

        output_thumbnail_path = os.path.join(os.path.dirname(video_path), 
                                             os.path.splitext(os.path.basename(video_path))[0] + '_thumbnail.jpg')

        # Abrir el archivo de video
        video_capture = cv2.VideoCapture(video_path)

        # Obtener el cuadro a 1 segundo
        video_capture.set(cv2.CAP_PROP_POS_MSEC, 1000)
        
        # Leer el cuadro
        success, frame = video_capture.read()

        if success:
            # Escalar el cuadro a 1000px de altura
            height, width, _ = frame.shape
            aspect_ratio = width / height
            new_height = 1000
            new_width = int(new_height * aspect_ratio)
            frame = cv2.resize(frame, (new_width, new_height))

            # Guardar el cuadro como miniatura
            cv2.imwrite(output_thumbnail_path, frame)

            print(f"Miniatura de video generada y guardada en: {output_thumbnail_path}")

            return output_thumbnail_path
        else:
            print("Error al leer el cuadro del video.")
            return None

    except Exception as e:
        print(f"Error inesperado al generar la miniatura del video: {e}")
        return None

@posts_bp.route('/posts', methods=['GET'])
@token_required
def get_posts():
    try:
        # Extract pagination parameters from query string
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))  # Puedes ajustar el valor predeterminado

        # Calcular el desplazamiento para recuperar la página correcta de datos
        offset = (page - 1) * per_page

        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute("""
            SELECT posts.id, posts.user_id, posts.img_raw, posts.img_compressed, posts.text, posts.created_at, posts.video_url, posts.video_thumbnail,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'upvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS upvotes,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'downvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS downvotes
            FROM posts
            LEFT JOIN user_votes uv ON posts.id = uv.post_id
            GROUP BY posts.id
            ORDER BY posts.created_at DESC  -- Ordenar por created_at en orden descendente
            LIMIT %s OFFSET %s
        """, (per_page, offset))

        posts = cursor.fetchall()

        db.close_connection()

        posts_data = [
            {
                'id': post[0],
                'user_id': post[1],
                'img_raw': post[2],
                'img_compressed': post[3],
                'text': post[4],
                'created_at': post[5],
                'video_url': post[6],
                'video_thumbnail': post[7],
                'upvotes': post[8],
                'downvotes': post[9]
            }
            for post in posts
        ]

        # No es necesario volver a ordenar los resultados en Python
        # Puesto que ya están ordenados en la consulta SQL

        return jsonify(posts_data)
    except Exception as e:
        logging.error(f"Error al recuperar las publicaciones: {str(e)}")
        return error_response('Error al recuperar las publicaciones', 500)

@posts_bp.route('/user/<string:username>/posts', methods=['GET'])
@token_required
def get_user_posts(username):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if user_id is None:
            db.close_connection()
            return error_response('User not found', 404)

        cursor.execute("""
            SELECT posts.id, posts.user_id, posts.img_raw, posts.img_compressed, posts.video_url, posts.video_thumbnail, posts.text, posts.created_at,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'upvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS upvotes,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'downvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS downvotes
            FROM posts
            LEFT JOIN user_votes uv ON posts.id = uv.post_id
            WHERE posts.user_id = %s
            GROUP BY posts.id
        """, (user_id[0],))

        posts = cursor.fetchall()

        db.close_connection()

        posts_data = [
            {
                'id': post[0],
                'user_id': post[1],
                'img_raw': post[2],
                'img_compressed': post[3],
                'video_url': post[4],
                'video_thumbnail': post[5],
                'text': post[6],
                'created_at': post[7],
                'upvotes': post[8],
                'downvotes': post[9]
            }
            for post in posts
        ]
        posts_data.sort(key=lambda post: post['created_at'], reverse=True)
        return jsonify(posts_data)
    except Exception as e:
        logging.error(f"Error retrieving user posts: {str(e)}")
        return error_response('Failed to retrieve user posts', 500)

@posts_bp.route('/post/<int:post_id>', methods=['GET'])
@token_required
def get_post(post_id):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute("""
            SELECT posts.id, posts.user_id, posts.img_raw, posts.img_compressed, posts.video_url, posts.video_thumbnail, posts.text, posts.created_at,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'upvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS upvotes,
            CAST(COALESCE(SUM(CASE WHEN uv.vote_type = 'downvote' THEN 1 ELSE 0 END), 0) AS SIGNED) AS downvotes
            FROM posts
            LEFT JOIN user_votes uv ON posts.id = uv.post_id
            WHERE posts.id = %s
            GROUP BY posts.id
        """, (post_id,))

        post = cursor.fetchone()

        db.close_connection()

        if post is None:
            return error_response('Post not found', 404)

        post_data = {
            'id': post[0],
            'user_id': post[1],
            'img_raw': post[2],
            'img_compressed': post[3],
            'video_url': post[4],
            'video_thumbnail': post[5],
            'text': post[6],
            'created_at': post[7],
            'upvotes': post[8],
            'downvotes': post[9]
        }

        return jsonify(post_data)
    except Exception as e:
        logging.error(f"Error retrieving post: {str(e)}")
        return error_response('Failed to retrieve post', 500)

@posts_bp.route('/post/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    try:
        db = DatabaseHandler()
        cursor = db.connection.cursor()

        cursor.execute("SELECT user_id FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()

        if not post:
            db.close_connection()
            return error_response('Post not found', 404)

        if post[0] != g.user_id:
            db.close_connection()
            return error_response('You are not authorized to delete this post', 403)

        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        db.connection.commit()

        db.close_connection()

        return jsonify(message='Post deleted successfully')
    except Exception as e:
        logging.error(f"Error deleting post: {str(e)}")
        return error_response('Failed to delete post', 500)

@posts_bp.route('/post/<int:post_id>/upvote', methods=['POST'])
@token_required
def upvote_post(post_id):
    return vote_post(post_id, 'upvote')

@posts_bp.route('/post/<int:post_id>/downvote', methods=['POST'])
@token_required
def downvote_post(post_id):
    return vote_post(post_id, 'downvote')

# The vote_post function (used by upvote and downvote routes) is the same as provided in the previous response.
def vote_post(post_id, vote_type):
    try:
        user_id = g.user_id

        if user_id is None:
            return error_response('Token is invalid or expired', 401)

        db = DatabaseHandler()
        cursor = db.connection.cursor()

        # Check if the user has already voted on this post
        cursor.execute(
            "SELECT * FROM user_votes WHERE user_id = %s AND post_id = %s",
            (user_id, post_id)
        )
        existing_vote = cursor.fetchone()

        if not existing_vote:
            # User hasn't voted on this post, so insert a new vote record.
            cursor.execute(
                "INSERT INTO user_votes (user_id, post_id, vote_type) VALUES (%s, %s, %s)",
                (user_id, post_id, vote_type)
            )
        else:
            # User has already voted on this post
            existing_vote_type = existing_vote[2]  # Assuming 'vote_type' is at index 2, replace with the actual index
            if existing_vote_type != vote_type:
                # Change the vote type
                cursor.execute(
                    "UPDATE user_votes SET vote_type = %s WHERE user_id = %s AND post_id = %s",
                    (vote_type, user_id, post_id)
                )
            else:
                # User is trying to vote with the same type, handle it here (e.g., return an error or other logic).
                db.close_connection()
                return error_response('User has already voted with the same type', 400)

        db.connection.commit()
        db.close_connection()

        return jsonify({'message': f'{vote_type.capitalize()} added successfully'})
    except Exception as e:
        logging.error(f"Error adding {vote_type}: {str(e)}")
        return error_response(f'Failed to add {vote_type}', 500)
    
# Define a function to generate a unique filename based on the current date and time
def generate_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    secure_name = secure_filename(filename)
    filename, file_extension = os.path.splitext(secure_name)
    
    # Generate random combination of numbers and letters
    random_combination = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    unique_filename = f"{filename}_{timestamp}_{random_combination}{file_extension}"
    return unique_filename
