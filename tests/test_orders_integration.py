import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.order_service import create_order_service
from app.repository.order_repository import get_all_orders
from app.core.database import TestingSessionLocal
from app.models.order_model import Order

client = TestClient(app)

# --- Mock functions for external API ---
async def mock_product_available(product_id):
    return {
        "id": product_id,
        "name": "Sample Product",
        "price": 100,
        "available_stock": 5
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

# --- Delete endpoint tests ---
def test_delete_order_success(db):
    # Create order
    order = Order(customer_name="Test Delete", product_id=1, quantity=1, total_price=100)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Delete order via API
    response = client.delete(f"/orders/{order.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Order {order.id} deleted successfully"}

def test_delete_order_not_found():
    response = client.delete("/orders/99999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

# --- Update endpoint tests ---
def test_update_order_success(db):
    # Create an order to update
    order = Order(customer_name="Before Update", product_id=1, quantity=1, total_price=100)
    db.add(order)
    db.commit()
    db.refresh(order)

    updated_data = {
        "customer_name": "After Update",
        "product_id": 1,
        "quantity": 3,
        "total_price": 150.0,  # ✅ corrected field name
        "status": "Pending"
    }

    # Call the PUT endpoint
    response = client.put(f"/orders/{order.id}", json=updated_data)

    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "After Update"
    assert data["quantity"] == 3
    assert data["total_price"] == 150.0  # ✅ corrected field name
    assert data["status"] == "Pending"



def test_update_order_not_found():
    updated_data = {
        "customer_name": "Nonexistent",
        "product_id": 2,
        "quantity": 1,
        "price": 120.0,
        "status":"Pending"
    }

    response = client.put("/orders/99999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_partial_update_order(db):
    # Create an order
    order = Order(customer_name="Partial Update", product_id=1, quantity=2, total_price=200 ,status="Pending")
    db.add(order)
    db.commit()
    db.refresh(order)

    # Only update quantity
    partial_data = {
        "quantity": 5
    }

    response = client.put(f"/orders/{order.id}", json=partial_data)
    assert response.status_code == 200
    data = response.json()

    assert data["quantity"] == 5
    assert data["customer_name"] == "Partial Update"  # unchanged
