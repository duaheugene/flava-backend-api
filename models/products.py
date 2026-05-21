from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    """Database model for food products."""
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(gt=0)  # Must be greater than 0
    image_url: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(index=True, max_length=100)  # e.g., "Starters", "Mains", "Drinks"
    is_available: bool = Field(default=True, index=True)
    restaurant_id: int = Field(foreign_key="restaurants.id", index=True)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Grilled Chicken Burger",
                "description": "Juicy grilled chicken with lettuce and tomato",
                "price": 8.99,
                "image_url": "https://cdn.example.com/products/burger.jpg",
                "category": "Mains",
                "is_available": True,
                "restaurant_id": 1,
            }
        }