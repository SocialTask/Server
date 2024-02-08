import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from backend.api import users, profile, follow, task, posts, auth

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_app()
        self.register_routes()
        self.register_error_handler()

    def configure_app(self):
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

    def register_routes(self):
        self.app.route('/assets/<path:filename>')(self.serve_static)
        self.app.route('/storage/<path:filename>')(self.serve_image)
        self.app.register_blueprint(users.users_bp)
        self.app.register_blueprint(profile.profile_bp)
        self.app.register_blueprint(follow.follow_bp)
        self.app.register_blueprint(task.task_bp)
        self.app.register_blueprint(posts.posts_bp)
        self.app.register_blueprint(auth.auth_bp)

    def register_error_handler(self):
        self.app.errorhandler(404)(self.not_found)

    def run(self, host='0.0.0.0', port=210, debug=True):
        self.app.run(host=host, port=port, debug=debug)

    def serve_static(self, filename):
        return send_from_directory('assets', filename)

    def serve_image(self, filename):
        return send_from_directory('storage', filename)

    def not_found(self, error):
        return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    server = Server()
    server.run()
