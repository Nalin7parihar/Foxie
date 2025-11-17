from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Base schema for product, containing common fields."""

    name: str
    price: float
    stock: int
    descrip: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(ProductBase):
    """Schema for updating an existing product, with all fields optional."""

    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    descrip: Optional[str] = None


class Product(ProductBase):
    """Main schema for product, including database-generated fields."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
