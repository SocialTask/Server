# RENAME THIS TO CONFIG.PY

FFMPEG_PATH = "" # Your FFMPEG Path
HOST = "0.0.0.0" # Your Server IP Default: 0.0.0.0
PORT = 80 # Your Server Port

# Database Configuration
DATABASE_CONFIG = {
    "host": "",
    "port": 3306,
    "user": "",
    "password": "",
    "database": "",
}

# Flask Configuration
SECRET_KEY = "" # Random Value (Numbers, Symbols, Letters)
BASE_URL = "" # Example: http://192.168.0.1:210

# CORS Configuration
CORS_CONFIG = {
    "resources": {r"/*": {"origins": "*"}}
}
