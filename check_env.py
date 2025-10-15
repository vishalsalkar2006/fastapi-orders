# check_env.py
from app.core.config import settings

print("APP_ENV:", settings.APP_ENV)
print("MYSQL_USER:", settings.MYSQL_USER)
print("MYSQL_PASSWORD:", settings.MYSQL_PASSWORD)
print("MYSQL_HOST:", settings.MYSQL_HOST)
print("MYSQL_DB:", settings.MYSQL_DB)
print("DATABASE_URL:", settings.DATABASE_URL)

