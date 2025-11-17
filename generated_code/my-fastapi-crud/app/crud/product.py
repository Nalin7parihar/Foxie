from typing import List, Union
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct:
    """CRUD operations for Product resources."""

    def get(self, db: Session, id: int) -> Product | None:
        """Retrieve a single product by its ID."""
        return db.get(Product, id)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve multiple products with pagination."""
        return db.scalars(select(Product).offset(skip).limit(limit)).all()

    def create(self, db: Session, obj_in: ProductCreate) -> Product:
        """Create a new product."""
        db_obj = Product(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: Product, obj_in: Union[ProductUpdate, dict]
    ) -> Product:
        """Update an existing product."""
        obj_data = (
            obj_in.model_dump(exclude_unset=True)
            if isinstance(obj_in, ProductUpdate)
            else obj_in
        )
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Product | None:
        """Delete a product by its ID."""
        obj = db.get(Product, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


product = CRUDProduct()
