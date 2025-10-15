# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # updated

# Use settings.DATABASE_URL instead of DATABASE_URL
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# For testing
TestingSessionLocal = SessionLocal

