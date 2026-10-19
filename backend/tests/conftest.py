
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db
from models import Product


@pytest.fixture(autouse=True)
def isolated_database():
    # Create a temporary SQLite database in memory
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    # Create database tables
    Base.metadata.create_all(bind=test_engine)

    # Insert demonstration products for this test
    with TestSessionLocal() as db:
        db.add_all([
            Product(
                product_id="demo-001",
                name="S2A_MSIL2A_20250731_DEMO_001",
                acquisition_date="2025-07-31",
                product_type="Sentinel-2 Level-2A",
                cloud_cover=2.85,
                availability="Available",
            ),
            Product(
                product_id="demo-002",
                name="S2B_MSIL2A_20250726_DEMO_002",
                acquisition_date="2025-07-26",
                product_type="Sentinel-2 Level-2A",
                cloud_cover=6.1,
                availability="Available",
            ),
            Product(
                product_id="demo-003",
                name="S2A_MSIL2A_20250721_DEMO_003",
                acquisition_date="2025-07-21",
                product_type="Sentinel-2 Level-2A",
                cloud_cover=9.4,
                availability="Available",
            ),
        ])

        db.commit()

    # Replace the API database dependency during tests
    def override_get_db():
        db = TestSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Execute the test
    try:
        yield
    finally:
        # Restore the normal dependency and clean up
        app.dependency_overrides.pop(get_db, None)
        test_engine.dispose()
