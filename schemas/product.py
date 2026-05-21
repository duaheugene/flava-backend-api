from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProductBase(BaseModel):
    """Base schema for product data."""
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(default=None, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price in USD")
    image_url: Optional[str] = Field(default=None, max_length=500, description="Product image URL")
    category: str = Field(..., max_length=100, description="Product category (e.g., Starters, Mains, Drinks)")
    is_available: bool = Field(default=True, description="Product availability status")

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        """Ensure price is positive and reasonable."""
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        if v > 999999.99:
            raise ValueError("Price exceeds maximum allowed value")
        return round(v, 2)

    @field_validator("name", "category")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace."""
        return v.strip() if isinstance(v, str) else v


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    restaurant_id: int = Field(..., description="Restaurant ID")

    @field_validator("restaurant_id")
    @classmethod
    def validate_restaurant_id(cls, v):
        """Ensure restaurant_id is positive."""
        if v <= 0:
            raise ValueError("restaurant_id must be positive")
        return v


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    is_available: Optional[bool] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        """Ensure price is positive and reasonable."""
        if v is None:
            return v
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        if v > 999999.99:
            raise ValueError("Price exceeds maximum allowed value")
        return round(v, 2)

    @field_validator("name", "category")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace."""
        return v.strip() if isinstance(v, str) else v


class ProductResponse(BaseModel):
    """Schema for product response data."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    category: str
    is_available: bool
    restaurant_id: int
    created_at: datetime
    updated_at: datetime

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
                "created_at": "2026-05-20T10:30:00",
                "updated_at": "2026-05-20T10:30:00",
            }
        }