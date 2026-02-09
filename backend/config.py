import os
from dotenv import load_dotenv

# Load environment variables from a .env file located in the same directory or parent directories
load_dotenv()

class Config:
    """
    Configuration class to centralize environment variable access.
    """
    # Secret key for Flask session management and cryptographic signing
    # Defaults to a dev key if not set (DO NOT use default in production)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_prod")
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
