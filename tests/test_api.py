# Тесты с PyTest

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_price():
    response = client.get("/crypto/price/bitcoin")
    assert response.status_code == 200
    assert "price" in response.json()

def test_add_crypto():
    response = client.post("/crypto/add", json={"coin": "testcoin", "price": 100.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Added/Updated"}

def test_view_crypto():
    # Сначала добавляем данные
    client.post("/crypto/add", json={"coin": "testview", "price": 200.0})
    response = client.get("/crypto/view/testview")
    assert response.status_code == 200
    assert "Price of testview: 200.0 USD" in response.text

@pytest.mark.asyncio
async def test_analyze():
    response = client.get("/crypto/analyze/bitcoin")
    assert response.status_code == 200
    assert "<div>" in response.text  # Plotly HTML

@pytest.mark.asyncio
async def test_demo_multitask():
    response = client.get("/crypto/demo-multitask")
    assert response.status_code == 200
    assert "async_results" in response.json()
