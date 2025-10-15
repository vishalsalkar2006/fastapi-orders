from app.models.order_model import Order
from sqlalchemy.orm import Session

def create_order(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: Session, order: Order):
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order: Order):
    db.delete(order)
    db.commit()

