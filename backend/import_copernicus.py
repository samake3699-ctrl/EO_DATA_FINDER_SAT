
from copernicus import search_sikasso_october
from database import SessionLocal
from models import Product


def import_products(products=None):
    if products is None:
        products = search_sikasso_october()
    inserted = 0

    with SessionLocal.begin() as db:
        for item in products:
            cloud = next(
                (
                    attr["Value"]
                    for attr in item.get("Attributes", [])
                    if attr.get("Name") == "cloudCover"
                ),
                None,
            )

            if cloud is None:
                continue

            existing = db.query(Product).filter_by(
                product_id=item["Id"]
            ).first()

            if existing:
                continue

            db.add(Product(
                product_id=item["Id"],
                name=item["Name"],
                acquisition_date=item["ContentDate"]["Start"][:10],
                product_type="Sentinel-2 Level-2A",
                cloud_cover=float(cloud),
                availability="Available" if item.get("Online") else "Unavailable",
            ))

            inserted += 1

    print(f"Products inserted: {inserted}")
    return inserted

if __name__ == "__main__":
    import_products()
