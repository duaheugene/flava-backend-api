from fastapi import FastAPI

from database import Base, engine
from models import user, products, categories  # noqa: F401 - ensures models are registered
from routes import auth, products as product_routes, categories as category_routes, menu

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Flava Backend API",
    description="Backend API system for food products, menu items, store products, categories, authentication, authorization, and SQLite integration.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(product_routes.router)
app.include_router(category_routes.router)
app.include_router(menu.router)


@app.get("/")
def home():
    return {
        "message": "Flava Backend API is running",
        "docs": "/docs",
        "features": [
            "Users",
            "Authentication",
            "Authorization",
            "Products",
            "Menu Items",
            "Categories",
            "Product Search",
            "Product Filtering",
            "SQLite Database",
        ],
    }
