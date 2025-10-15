# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Main engine
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Base class for models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Optional: separate session for testing (can point to test DB)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

