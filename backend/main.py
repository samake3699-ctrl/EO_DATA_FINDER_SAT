from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

DEMO_PRODUCTS = [
    {
        "id": "demo-001",
        "name": "S2A_MSIL2A_20250731_DEMO_001",
        "acquisitionDate": "2025-07-31",
        "productType": "Sentinel-2 Level-2A",
        "cloudCover": 2.85,
        "availability": "Available",
    },
    {
        "id": "demo-002",
        "name": "S2B_MSIL2A_20250726_DEMO_002",
        "acquisitionDate": "2025-07-26",
        "productType": "Sentinel-2 Level-2A",
        "cloudCover": 6.1,
        "availability": "Available",
    },
    {
        "id": "demo-003",
        "name": "S2A_MSIL2A_20250721_DEMO_003",
        "acquisitionDate": "2025-07-21",
        "productType": "Sentinel-2 Level-2A",
        "cloudCover": 9.4,
        "availability": "Available",
    },
]


@app.get("/")
def read_root():
    return {
        "message": "EO Data Finder API is running"
    }


@app.get("/api/products")
def get_products():
    return DEMO_PRODUCTS