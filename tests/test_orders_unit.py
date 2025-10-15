import pytest
from app.models.order_model import Order

def test_order_model_create():
    order = Order(customer_name="Vishal", product_id=1, quantity=2, total_price=100.0)
    assert order.customer_name == "Vishal"
    assert order.quantity == 2

