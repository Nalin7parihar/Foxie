from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db_session import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.product import product as crud_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of products."""
    products = crud_product.get_multi(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by its ID."""
    db_obj = crud_product.get(db, id=product_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_obj


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    new_obj = crud_product.create(db, obj_in=product_in)
    return new_obj


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)
):
    """Update an existing product by its ID."""
    db_obj = crud_product.get(db, id=product_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    updated_obj = crud_product.update(db, db_obj=db_obj, obj_in=product_in)
    return updated_obj


@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product by its ID."""
    db_obj = crud_product.get(db, id=product_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    removed_obj = crud_product.remove(db, id=product_id)
    return removed_obj
