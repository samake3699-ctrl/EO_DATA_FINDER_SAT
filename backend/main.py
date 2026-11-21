from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Literal
from pathlib import Path
from fastapi.responses import FileResponse
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
            "geoFootprint": product.get("GeoFootprint"),
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

# Sprint 4 - Real NDVI and CHIRPS analysis results

@app.get("/api/analysis/results")
def get_analysis_results():
    from analysis_results import get_ndvi_results, get_chirps_results

    try:
        return {
            "ndviAnalysis": get_ndvi_results(),
            "rainfallAnalysis": get_chirps_results()
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Required analysis data file is missing."
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=503,
            detail="Analysis data is invalid or unavailable."
        ) from exc


# Sprint 4 - Serve the real Sentinel-2 NDVI preview

@app.get("/api/analysis/ndvi-preview")
def get_ndvi_preview():
    image_path = (
        Path(__file__).resolve().parent
        / "data"
        / "sentinel2"
        / "sikasso_20251028_ndvi_preview.png"
    )

    if not image_path.is_file():
        raise HTTPException(
            status_code=503,
            detail="NDVI preview image is unavailable."
        )

    return FileResponse(
        path=image_path,
        media_type="image/png"
    )


# Sprint 4 - Serve the real CHIRPS rainfall chart

@app.get("/api/analysis/chirps-chart")
def get_chirps_chart():
    chart_path = (
        Path(__file__).resolve().parent
        / "data"
        / "chirps"
        / "sikasso_chirps_comparison.png"
    )

    if not chart_path.is_file():
        raise HTTPException(
            status_code=503,
            detail="CHIRPS rainfall chart is unavailable."
        )

    return FileResponse(
        path=chart_path,
        media_type="image/png"
    )

# Sprint 4 - Analysis results for a selected product

@app.get("/api/analysis/products/{product_id}")
def get_selected_product_analysis(product_id: str):
    import json
    from uuid import UUID
    from analysis_results import get_chirps_results

    try:
        product_id = str(UUID(product_id))
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid product ID."
        )

    result_file = (
        Path(__file__).resolve().parent
        / "data"
        / "sentinel2"
        / f"{product_id}_analysis.json"
    )

    if not result_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="NDVI analysis not found for this product."
        )

    try:
        result = json.loads(
            result_file.read_text(encoding="utf-8")
        )

        if result.get("productId") != product_id:
            raise ValueError("Product ID mismatch.")

        rainfall = get_chirps_results()

        return {
            "ndviAnalysis": {
                "productId": product_id,
                "productName": result["productName"],
                "acquisitionDate": result["acquisitionDate"],
                "source": "Sentinel-2 Level-2A",
                "ndvi": result["ndvi"]
            },
            "rainfallAnalysis": rainfall
        }

    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Analysis data is invalid."
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Required CHIRPS data is missing."
        ) from exc

# Sprint 4 - Prepare the selected product automatically

@app.post("/api/analysis/products/{product_id}/prepare")
def prepare_selected_product_analysis(product_id: str):
    from uuid import UUID
    from download_selected_product import download_selected_product
    from calculate_selected_ndvi import calculate_selected_ndvi

    try:
        product_id = str(UUID(product_id))
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid product ID."
        )

    data_dir = (
        Path(__file__).resolve().parent
        / "data"
        / "sentinel2"
    )

    bands_file = data_dir / f"{product_id}_with_scl.tif"
    results_file = data_dir / f"{product_id}_analysis.json"
    preview_file = data_dir / f"{product_id}_ndvi_preview.png"

    # Download only if needed
    if not bands_file.is_file():
        download_selected_product(product_id)

    # Calculate only if results or preview are missing
    if not results_file.is_file() or not preview_file.is_file():
        calculate_selected_ndvi(product_id)

    return {
        "status": "ready",
        "productId": product_id
    }

# Sprint 4 - NDVI preview for the selected product

@app.get("/api/analysis/products/{product_id}/ndvi-preview")
def get_selected_ndvi_preview(product_id: str):
    from uuid import UUID

    try:
        product_id = str(UUID(product_id))
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid product ID."
        )

    image_path = (
        Path(__file__).resolve().parent
        / "data"
        / "sentinel2"
        / f"{product_id}_ndvi_preview.png"
    )

    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="NDVI map not found for the selected product."
        )

    return FileResponse(
        path=image_path,
        media_type="image/png"
    )
