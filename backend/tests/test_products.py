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


# Sprint 2: Date filtering tests

def test_filter_products_full_date_range():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-07-01",
            "end_date": "2025-08-01",
            "max_cloud": 10,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_filter_products_one_date_match():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-07-28",
            "end_date": "2025-08-01",
            "max_cloud": 10,
        },
    )

    assert response.status_code == 200

    products = response.json()
    assert len(products) == 1
    assert products[0]["id"] == "demo-001"


def test_filter_products_two_date_matches():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-07-20",
            "end_date": "2025-07-29",
            "max_cloud": 10,
        },
    )

    assert response.status_code == 200

    product_ids = {p["id"] for p in response.json()}
    assert product_ids == {"demo-002", "demo-003"}


def test_filter_products_no_date_match():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-08-01",
            "end_date": "2025-08-15",
            "max_cloud": 10,
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_reject_invalid_date_range():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-08-01",
            "end_date": "2025-07-01",
        },
    )

    assert response.status_code == 422


def test_reject_invalid_date_format():
    response = client.get(
        "/api/products",
        params={
            "start_date": "2025-99-99",
            "end_date": "2025-08-01",
        },
    )

    assert response.status_code == 422


# Sprint 2: Pilot area validation tests

def test_supported_pilot_area():
    response = client.get(
        "/api/products",
        params={
            "area": "sikasso",
            "start_date": "2025-07-01",
            "end_date": "2025-08-01",
            "max_cloud": 10,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_reject_unsupported_pilot_areas():
    for area in ["bamako", "kayes", "mali"]:
        response = client.get(
            "/api/products",
            params={"area": area},
        )

        assert response.status_code == 422
