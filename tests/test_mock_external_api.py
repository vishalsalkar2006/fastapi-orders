import pytest
from app.services.order_service import create_order_service

class MockDB:
    def commit(self): pass
    def add(self, x): pass
    def refresh(self, x): pass

async def mock_fetch_product(_):
    return {"id": 1, "price": 50.0, "available_stock": 20}

@pytest.mark.asyncio
async def test_create_order_with_mock(monkeypatch):
    monkeypatch.setattr("app.services.order_service.fetch_product_details", mock_fetch_product)
    db = MockDB()
    order_data = type("obj", (), {"customer_name": "Vishal", "product_id": 1, "quantity": 2})
    order = await create_order_service(db, order_data)
    assert order.total_price == 100.0

