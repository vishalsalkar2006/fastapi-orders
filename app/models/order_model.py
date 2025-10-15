from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String, nullable=False, default="Pending")  # ✅ Default adde

