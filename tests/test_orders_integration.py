# tests/test_orders_integration.py
import pytest
from app.services.order_service import create_order_service
from app.repository.order_repository import get_all_orders
from app.core.database import TestingSessionLocal

# --- Mock functions for external API ---
async def mock_product_available(product_id):
    return {
        "id": product_id,
        "name": "Sample Product",
        "price": 100,
        "available_stock": 5  # change key from "stock" -> "available_stock"
    }

async def mock_product_out_of_stock(product_id):
    return {
        "id": product_id,
        "name": "Sample Product",
        "price": 100,
        "available_stock": 0
    }

async def mock_product_api_error(product_id):
    return {
        "id": product_id,
        "name": "Sample Product",
        "price": 0,
        "available_stock": 10
    }

# --- Fixtures ---
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Tests ---
@pytest.mark.asyncio
async def test_create_order_success(monkeypatch, db):
    # Patch external API
    monkeypatch.setattr(
        "app.services.order_service.fetch_product_details",
        mock_product_available
    )

    order_data = type("obj", (), {
        "customer_name": "Vishal",
        "product_id": 1,
        "quantity": 2
    })

    order = await create_order_service(db, order_data)
    assert order.total_price == 200
    assert order.status == "Pending"

@pytest.mark.asyncio
async def test_create_order_out_of_stock(monkeypatch, db):
    monkeypatch.setattr(
        "app.services.order_service.fetch_product_details",
        mock_product_out_of_stock
    )

    order_data = type("obj", (), {
        "customer_name": "Vishal",
        "product_id": 1,
        "quantity": 2
    })

    with pytest.raises(Exception) as exc:
        await create_order_service(db, order_data)
    assert "Insufficient stock" in str(exc.value)

@pytest.mark.asyncio
async def test_create_order_api_error(monkeypatch, db):
    monkeypatch.setattr(
        "app.services.order_service.fetch_product_details",
        mock_product_api_error
    )

    order_data = type("obj", (), {
        "customer_name": "Vishal",
        "product_id": 1,
        "quantity": 2
    })

    order = await create_order_service(db, order_data)
    # Price is 0 due to API failure
    assert order.total_price == 0
    assert order.status == "Pending"
