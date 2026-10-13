from database import Base, SessionLocal, engine
from models import Product


def seed_products():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    try:
        existing_products = db.query(Product).count()

        if existing_products > 0:
            print(
                f"Database already contains {existing_products} product(s)."
            )
            return

        products = [
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
        ]

        db.add_all(products)
        db.commit()

        print("3 demonstration products inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()