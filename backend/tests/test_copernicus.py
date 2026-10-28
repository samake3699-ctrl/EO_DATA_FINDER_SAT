
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_reject_invalid_copernicus_product_id():
    response = client.post(
        "/api/copernicus/products/not-a-uuid/save"
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid Copernicus product ID."

def test_copernicus_search_sends_filters(monkeypatch):

    def fake_search(start_date, end_date, max_cloud):
        assert start_date == "2025-10-01"
        assert end_date == "2025-11-01"
        assert max_cloud == 5.0
        return []

    monkeypatch.setattr(
        "copernicus.search_sikasso_october",
        fake_search
    )

    response = client.get(
        "/api/copernicus/products",
        params={
            "start_date": "2025-10-01",
            "end_date": "2025-10-31",
            "max_cloud": 5
        }
    )

    assert response.status_code == 200
    assert response.json() == []

def test_copernicus_product_metadata(monkeypatch):
    fake_product = {
        "Id": "11111111-1111-4111-8111-111111111111",
        "Name": "S2A_MSIL2A_TEST_PRODUCT",
        "ContentDate": {
            "Start": "2025-10-15T10:50:31.000Z"
        },
        "Online": True,
        "Attributes": [
            {"Name": "cloudCover", "Value": 3.5}
        ]
    }

    monkeypatch.setattr(
        "copernicus.search_sikasso_october",
        lambda **kwargs: [fake_product]
    )

    response = client.get("/api/copernicus/products")

    assert response.status_code == 200

    product = response.json()[0]

    assert product["acquisitionDate"] == "2025-10-15"
    assert product["cloudCover"] == 3.5
    assert product["availability"] == "Available"

def test_copernicus_import_avoids_duplicates(monkeypatch, tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from models import Product
    import import_copernicus

    engine = create_engine(
        f"sqlite:///{tmp_path / 'copernicus_test.db'}"
    )
    Base.metadata.create_all(bind=engine)

    TestSession = sessionmaker(bind=engine)
    monkeypatch.setattr(
        import_copernicus, "SessionLocal", TestSession
    )

    fake_product = {
        "Id": "22222222-2222-4222-8222-222222222222",
        "Name": "S2A_MSIL2A_TEST_PRODUCT",
        "ContentDate": {
            "Start": "2025-10-15T10:50:31.000Z"
        },
        "Online": True,
        "Attributes": [
            {"Name": "cloudCover", "Value": 3.5}
        ]
    }

    assert import_copernicus.import_products([fake_product]) == 1
    assert import_copernicus.import_products([fake_product]) == 0

    with TestSession() as db:
        assert db.query(Product).count() == 1

    engine.dispose()
