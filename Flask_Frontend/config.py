import os

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'MY_API_KEY')  # Use environment variable or default value
    FASTAPI_URL = os.environ.get('FASTAPI_URL', 'http://localhost:8000')  # URL of your FastAPI backend

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Ensure this is set in the production environment
    FASTAPI_URL = os.environ.get('FASTAPI_URL')  # Ensure this is set in the production environment
