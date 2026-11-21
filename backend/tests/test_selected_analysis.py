
import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

INVALID_ID = "invalid-product-id"

MISSING_ID = "00000000-0000-0000-0000-000000000000"


@pytest.mark.parametrize("method,path", [
    ("GET", f"/api/analysis/products/{INVALID_ID}"),
    ("POST", f"/api/analysis/products/{INVALID_ID}/prepare"),
    ("GET", f"/api/analysis/products/{INVALID_ID}/ndvi-preview"),
])
def test_invalid_product_id(method, path):
    response = client.request(method, path)
    assert response.status_code == 422


@pytest.mark.parametrize("path", [
    f"/api/analysis/products/{MISSING_ID}",
    f"/api/analysis/products/{MISSING_ID}/ndvi-preview",
])
def test_missing_analysis_returns_404(path):
    response = client.get(path)
    assert response.status_code == 404
