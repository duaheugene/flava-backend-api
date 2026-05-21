from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(..., gt=0)
    image_url: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(..., min_length=1, max_length=100)
    is_available: bool = True
    store_name: str = Field(..., min_length=1, max_length=150)

    @field_validator("name", "category", "store_name")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return round(value, 2)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[float] = Field(default=None, gt=0)
    image_url: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    is_available: Optional[bool] = None
    store_name: Optional[str] = Field(default=None, min_length=1, max_length=150)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    category: str
    is_available: bool
    store_name: str
    created_at: datetime
    updated_at: Optional[datetime]
