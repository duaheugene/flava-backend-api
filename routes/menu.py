from typing import Generator, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select

from models.products import Product
from schemas.product import ProductResponse


router = APIRouter(prefix="/menu", tags=["menu"])


def get_db() -> Generator:
    """Dependency for database session management."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=Dict[str, List[ProductResponse]],
    summary="Get menu for a restaurant"
)
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the complete menu for a restaurant, organized by category.

    Products are automatically filtered to show only available items.

    **Response format**:
    ```json
    {
        "Starters": [...],
        "Mains": [...],
        "Drinks": [...]
    }
    ```
    """
    # Fetch all available products for the restaurant
    statement = select(Product).where(
        Product.restaurant_id == restaurant_id,
        Product.is_available == True
    ).order_by(Product.category, Product.name)

    products = db.exec(statement).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No available products found for restaurant {restaurant_id}"
        )

    # Group products by category
    menu: Dict[str, List[ProductResponse]] = {}
    for product in products:
        category = product.category
        if category not in menu:
            menu[category] = []
        menu[category].append(ProductResponse.model_validate(product))

    return menu