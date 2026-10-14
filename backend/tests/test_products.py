from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "EO Data Finder API is running"

def test_get_all_products():
    response = client.get("/api/products?max_cloud=100")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 3


def test_filter_products_with_max_cloud_10():
    response = client.get("/api/products?max_cloud=10")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 3


def test_filter_products_with_max_cloud_5():
    response = client.get("/api/products?max_cloud=5")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 1
    assert products[0]["id"] == "demo-001"


def test_filter_products_with_max_cloud_2():
    response = client.get("/api/products?max_cloud=2")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 0


def test_reject_invalid_max_cloud():
    response = client.get("/api/products?max_cloud=150")

    assert response.status_code == 422