from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
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
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

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