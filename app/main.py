# app/main.py
from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.orders_router import router as orders_router  # Import the router object

app = FastAPI()

# Include routers
app.include_router(orders_router)

# Create tables (only if they don't exist)
Base.metadata.create_all(bind=engine)

