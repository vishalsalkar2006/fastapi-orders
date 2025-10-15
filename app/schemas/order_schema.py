from pydantic import BaseModel, conint, constr

class OrderCreate(BaseModel):
    customer_name: constr(min_length=1)
    product_id: int
    quantity: conint(gt=0)

class OrderUpdate(BaseModel):
    quantity: int | None = None
    status: str | None = None

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        orm_mode = True

