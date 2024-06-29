import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    API_KEY: str = os.getenv("API_KEY")
    JWT_KEY:str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGO:str = os.getenv("JWT_ALGORITHM")
    TOKEN_EXPIRATION: int = int(os.getenv("TOKEN_EXPIRATION", 30))
settings = Settings()