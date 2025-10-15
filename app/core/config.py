# app/core/config.py
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load appropriate env file
env_file = ".env.test" if os.getenv("APP_ENV") == "test" else ".env"
load_dotenv(env_file)

class Settings:
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = quote_plus(os.getenv("MYSQL_PASSWORD"))
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    APP_ENV: str = os.getenv("APP_ENV")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))

settings = Settings()

