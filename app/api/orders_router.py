from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.services import order_service
from app.repository import order_repository
from app.core.database import SessionLocal

router = APIRouter(prefix="/orders", tags=["Orders"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return await order_service.create_order_service(db, order)


# READ (Get all)
@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return order_repository.get_all_orders(db)


# READ (Get one)
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_repository.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ✅ Full update (PUT)
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, updated_order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in updated_order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order


# ✅ Partial update (PATCH)
@router.patch("/{order_id}", response_model=OrderResponse)
def partial_update_order(order_id: int, updated_fields: dict, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in updated_fields.items():
        if hasattr(db_order, key):
            setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order




# DELETE
@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}
