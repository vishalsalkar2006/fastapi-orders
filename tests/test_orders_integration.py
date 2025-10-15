import pytest
from app.services.order_service import create_order_service
from app.core.database import TestingSessionLocal

# Mock external API
async def mock_fetch_product(product_id):
    return {"id": product_id, "price": 50.0, "available_stock": 20}

@pytest.mark.asyncio
async def test_create_order_integration(monkeypatch):
    # Patch fetch_product_details where order_service imports it
    monkeypatch.setattr(
        "app.services.order_service.fetch_product_details",
        mock_fetch_product
    )

    db = TestingSessionLocal()
    order_data = type("obj", (), {
        "customer_name": "Vishal",
        "product_id": 1,
        "quantity": 2
    })

    order = await create_order_service(db, order_data)

    assert order.total_price == 100.0
    assert order.status == "Pending"

