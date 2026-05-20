# Flava Backend API

A backend API project inspired by Flava Delivery and modern food delivery/e-commerce systems.

## Project Focus

Build APIs for:

- Food products
- Menu items
- Store products
- Product categories
- Users
- Authentication and authorization
- Product search and filtering
- SQLite database integration

## Project Structure

```text
flava_backend_api/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── products.py
│   └── categories.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── products.py
│   ├── categories.py
│   └── menu.py
│
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
│
├── services/
│   ├── __init__.py
│   └── auth_services.py
│
├── database.py
├── main.py
├── requirements.txt
└── README.md
```

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
uvicorn main:app --reload
```

3. Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Main Endpoints

### Authentication

- `POST /auth/register` - register a user
- `POST /auth/login` - login and receive access token

### Products

- `POST /products/` - create product
- `GET /products/` - get all products
- `GET /products/{product_id}` - get one product
- `PUT /products/{product_id}` - update product
- `DELETE /products/{product_id}` - delete product

### Categories

- `POST /categories/` - create category
- `GET /categories/` - get all categories
- `GET /categories/{category_id}` - get one category
- `DELETE /categories/{category_id}` - delete category

### Menu

- `GET /menu/` - get available menu items
- `GET /menu/stores` - get stores selling products

## Team Task Division

1. User Models, Authentication & Authorization
   - `models/user.py`
   - `schemas/user.py`
   - `routes/auth.py`
   - `services/auth_services.py`

2. Product Models, Menu & CRUD Routes
   - `models/products.py`
   - `schemas/product.py`
   - `routes/products.py`
   - `routes/menu.py`

3. Categories & Product Filtering/Search
   - `models/categories.py`
   - `routes/categories.py`

4. SQLite Database Integration
   - `database.py`

5. Integration, Testing & Main App
   - `main.py`
   - `README.md`

## Notes

Protected routes require login. First register a user, then login to get a bearer token. Use the token inside Swagger UI by clicking **Authorize**.
