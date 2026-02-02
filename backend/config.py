import os
from dotenv import load_dotenv

# Load environment variables from a .env file located in the same directory or parent directories
load_dotenv()

class Config:
    """
    Configuration class to centralize environment variable access.
    """
    # URL for the Supabase instance
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    
    # Public API key for Supabase (anon key)
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Secret key for Flask session management and cryptographic signing
    # Defaults to a dev key if not set (DO NOT use default in production)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_prod")
