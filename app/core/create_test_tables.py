# app/core/create_test_tables.py
from app.core.database import engine
from app.models.order_model import Base  # make sure Base is imported from your models

Base.metadata.create_all(bind=engine)
print("Tables created in test DB!")

