# RENAME THIS TO CONFIG.PY
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
