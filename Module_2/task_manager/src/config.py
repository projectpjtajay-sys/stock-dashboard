import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "dev")
load_dotenv(dotenv_path=f"./src/env_files/{ENV}/.env")
class Settings:
    PROJECT_NAME: str = "Task Manager"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()