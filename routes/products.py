from datetime import datetime
from typing import Generator
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select

from models.products import Product
from schemas.product import ProductCreate, ProductUpdate, ProductResponse


router = APIRouter(prefix="/products", tags=["products"])


def get_db() -> Generator:
    """Dependency for database session management."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product.

    **Authentication**: Admin/Merchant only (add dependency as needed)
    """
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        category=product_data.category,
        is_available=product_data.is_available,
        restaurant_id=product_data.restaurant_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Retrieve a product by ID"
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Fetch a single product by ID."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product"
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing product.

    **Authentication**: Admin/Merchant only (add dependency as needed)
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product"
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.

    **Authentication**: Admin/Merchant only (add dependency as needed)
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    db.delete(product)
    db.commit()