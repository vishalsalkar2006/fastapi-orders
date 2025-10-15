from app.repository import order_repository
from app.utils.external_api_client import fetch_product_details
from app.models.order_model import Order
from fastapi import HTTPException, status

async def create_order_service(db, order_data):
    product = await fetch_product_details(order_data.product_id)

    if not product or product["available_stock"] < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    total_price = product["price"] * order_data.quantity

    order = Order(
        customer_name=order_data.customer_name,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price,
        status="Pending",
    )
    return order_repository.create_order(db, order)

