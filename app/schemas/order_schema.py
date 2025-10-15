from pydantic import BaseModel, conint, constr
from typing import Optional  # ✅ add this line

class OrderCreate(BaseModel):
    customer_name: constr(min_length=1)
    product_id: int
    quantity: conint(gt=0)

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product_id: int
    quantity: int
    total_price: float
    status: str

    model_config = {
        "from_attributes": True  # ✅ Pydantic v2 version of orm_mode
    }
