from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.products import Product
from schemas.product import ProductResponse

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/", response_model=dict[str, list[ProductResponse]])
def get_menu(db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .order_by(Product.category, Product.name)
        .all()
    )

    menu = defaultdict(list)
    for product in products:
        menu[product.category].append(ProductResponse.model_validate(product))

    return dict(menu)


@router.get("/store/{store_name}", response_model=dict[str, list[ProductResponse]])
def get_store_menu(store_name: str, db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.store_name.ilike(store_name), Product.is_available == True)
        .order_by(Product.category, Product.name)
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No available products found for store '{store_name}'",
        )

    menu = defaultdict(list)
    for product in products:
        menu[product.category].append(ProductResponse.model_validate(product))

    return dict(menu)


@router.get("/stores", response_model=list[str])
def get_stores(db: Session = Depends(get_db)):
    rows = db.query(Product.store_name).distinct().order_by(Product.store_name).all()
    return [row[0] for row in rows]
