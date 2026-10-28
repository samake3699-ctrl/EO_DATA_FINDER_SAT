from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Literal

from sqlalchemy.orm import Session

import models

from database import Base, SessionLocal, engine

app = FastAPI(
    title="EO Data Finder API",
    version="0.1.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {
        "message": "EO Data Finder API is running"
    }


@app.get("/api/products")
def get_products(
    area: Literal["sikasso"] = Query(
        default="sikasso",
        description="Supported pilot area: Sikasso, Mali",
    ),
    max_cloud: float = Query(
        default=100,
        ge=0,
        le=100,
        description="Maximum cloud coverage percentage",
    ),
    start_date: date | None = Query(
        default=None,
        description="Start date in YYYY-MM-DD format",
    ),
    end_date: date | None = Query(
        default=None,
        description="End date in YYYY-MM-DD format",
    ),
    db: Session = Depends(get_db),
):
    # Validate the date range
    if start_date and end_date and start_date >= end_date:
        raise HTTPException(
            status_code=422,
            detail="The end date must be after the start date.",
        )

    # Start building the database query
    query = db.query(models.Product)

    # Filter by cloud coverage
    query = query.filter(
        models.Product.cloud_cover <= max_cloud
    )

    # Filter by start date
    if start_date:
        query = query.filter(
            models.Product.acquisition_date >= start_date.isoformat()
        )

    # Filter by end date
    if end_date:
        query = query.filter(
            models.Product.acquisition_date <= end_date.isoformat()
        )

    # Execute database query
    products = query.all()

    # Return results to React
    return [
        {
            "id": product.product_id,
            "name": product.name,
            "acquisitionDate": product.acquisition_date,
            "productType": product.product_type,
            "cloudCover": product.cloud_cover,
            "availability": product.availability,
        }
        for product in products
    ]


@app.get("/api/copernicus/products")
def get_copernicus_products(
    start_date: date = Query(default=date(2025, 10, 1)),
    end_date: date = Query(default=date(2025, 10, 31)),
    max_cloud: float = Query(default=10.0, ge=0, le=100),
):
    from datetime import timedelta
    from copernicus import search_sikasso_october

    if start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="End date must not precede start date.",
        )

    products = search_sikasso_october(
        start_date=start_date.isoformat(),
        end_date=(end_date + timedelta(days=1)).isoformat(),
        max_cloud=max_cloud,
    )

    return [
        {
            "id": product["Id"],
            "name": product["Name"],
            "acquisitionDate": product["ContentDate"]["Start"][:10],
            "productType": "Sentinel-2 Level-2A",
            "availability": "Available" if product.get("Online") else "Unavailable",
            
"cloudCover": next(
    (
        attribute["Value"]
        for attribute in product.get("Attributes", [])
        if attribute.get("Name") == "cloudCover"
    ),
    None,
),

        }
        for product in products
    ]

@app.post("/api/copernicus/products/{product_id}/save")
def save_copernicus_product(product_id: str):
    from uuid import UUID
    from copernicus import get_product_by_id
    from import_copernicus import import_products

    try:
        product_id = str(UUID(product_id))
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid Copernicus product ID.",
        )

    product = get_product_by_id(product_id)

    if "MSIL2A" not in product.get("Name", ""):
        raise HTTPException(
            status_code=422,
            detail="Only Sentinel-2 Level-2A products are supported.",
        )

    inserted = import_products([product])

    return {
        "status": "saved" if inserted == 1 else "already_exists",
        "productId": product_id,
    }
