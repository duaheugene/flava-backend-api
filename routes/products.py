from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models.products import Product
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from services.auth_services import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    search: str | None = Query(default=None, description="Search by product name"),
    category: str | None = Query(default=None, description="Filter by category"),
    store_name: str | None = Query(default=None, description="Filter by store name"),
    available_only: bool = Query(default=False, description="Show only available products"),
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category.ilike(category))
    if store_name:
        query = query.filter(Product.store_name.ilike(store_name))
    if available_only:
        query = query.filter(Product.is_available == True)

    return query.order_by(Product.name).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    update_data = product_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
