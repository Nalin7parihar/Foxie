from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_model import Base


class Product(Base):
    """SQLAlchemy model for a product."""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    descrip: Mapped[str] = mapped_column(String, nullable=True)
