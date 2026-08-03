# Secure Product API

A FastAPI-based REST API for managing users and products with JWT authentication, role-based access control (RBAC), and MongoDB for persistence.

## What's included

- User registration and login with JWT access and refresh tokens
- Role-based access control (user / admin)
- Protected endpoints for profile and admin operations
- Product CRUD (create, read, update, delete)
- Product price filtering using data from the external FakeStore API
- Admin endpoints for promoting users and viewing basic statistics
- Password hashing with bcrypt
- Pydantic schemas for request/response validation
- MongoDB integration for persistent storage
- Automatic API docs via OpenAPI/Swagger

## Tech stack

- Framework: FastAPI
- ASGI server: Uvicorn
- Database: MongoDB
- Auth: JWT (OAuth2PasswordBearer)
- Password hashing: bcrypt (passlib)
- HTTP client for external API: requests
- Environment management: python-dotenv

## Project structure

```
secure-product-api/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── core/
│   ├── config.py           # Configuration constants (SECRET_KEY, ALGORITHM, token expiration)
│   └── security.py         # Security utilities (password hashing, JWT token creation)
├── routers/
│   ├── auth.py             # Authentication endpoints (register, login, refresh token)
│   ├── products.py         # Product management endpoints (CRUD operations)
│   └── admin.py            # Admin operations (user promotion, dashboard statistics)
├── database/
│   └── connection.py       # MongoDB connection and collection definitions
└── schemas/
    ├── user.py             # User request/response schemas
    └── product.py          # Product request/response schemas
```

## Prerequisites

- Python 3.7+
- MongoDB running locally or remotely
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hridaykp/secure-product-api.git
cd secure-product-api
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is running. Example using Docker:

```bash
docker run -d -p 27017:27017 mongo
```

4. Create a .env file or set environment variables used by core/config.py (SECRET_KEY, MONGO_URI, etc.).

## Running the app

Start the server with:

```bash
uvicorn main:app --reload
```

Open API docs at http://localhost:8000/docs (Swagger UI) or http://localhost:8000/redoc.

## Endpoints (summary)

- GET /                — Home
- GET /about           — About

Authentication

- POST /register
  - Body: { "username": "string", "password": "string" }
  - Response: message on successful registration

- POST /login
  - Form data: username, password
  - Response: { "access_token": "string", "refresh_token": "string", "token_type": "bearer" }
  - Access token: short-lived (configured in core/config.py)
  - Refresh token: longer-lived (configured in core/config.py)

- POST /refresh-token
  - Body: { "refresh_token": "string" }
  - Response: { "access_token": "string", "token_type": "bearer" }

- GET /profile
  - Requires Authorization: Bearer <access_token>
  - Returns current user profile (id, username, role)

Products

- GET /products
  - Fetch all products stored in MongoDB

- GET /products/id/{id}
  - Fetch product by MongoDB ObjectId

- GET /products/price/{price}
  - Fetch products in a price range (uses fakestoreapi.com for price-based filtering)

- POST /products
  - Body: { "name": "string", "price": float }
  - Create a new product

- PUT /products/{prod_id}
  - Update existing product by id

- DELETE /products/{prod_id}
  - Delete product by id

Admin

- POST /admin/make-admin/{username}
  - Promote a user to admin (admin role required)

- GET /admin/dashboard
  - Returns basic statistics (total users, total admins) and current admin username (admin role required)

## Data model (collections)

Users collection:

```json
{
  "_id": "ObjectId",
  "username": "string",
  "password": "string (bcrypt hashed)",
  "role": "string (user|admin)"
}
```

Products collection:

```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "float"
}
```

## Configuration

Edit core/config.py to set values such as:

```python
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 15
```

Ensure the MongoDB URI in database/connection.py or your environment is correct (e.g. mongodb://localhost:27017).

## Notes & testing

- Use the built-in Swagger UI to try protected endpoints. For endpoints that require an access token, first obtain tokens from /login.
- Passwords are stored hashed with bcrypt — keep SECRET_KEY secure in production.

## Contributing

Contributions, bug reports and pull requests are welcome.

## License

MIT
