import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')  # Provide a default
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db') # Provide a default
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False # Consider setting this based on environment (e.g., True in production)
