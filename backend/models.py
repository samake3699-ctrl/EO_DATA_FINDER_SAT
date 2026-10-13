from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String)

    acquisition_date: Mapped[str] = mapped_column(String)

    product_type: Mapped[str] = mapped_column(String)

    cloud_cover: Mapped[float] = mapped_column(Float)

    availability: Mapped[str] = mapped_column(String)