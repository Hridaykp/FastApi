from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import admin, auth, products

app = FastAPI(
    title="Secure Product Management API",
    version="1.0.0",
    description="""
            Backend API built with FastAPI featuring:
            - JWT-based authentication
            - RBAC
            - Product CRUD ops
            - Secure database integration
            """
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific URLs for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for authentication, product management and admin
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(admin.router) 


# General endpoints 
@app.get("/", tags=["General"])
def home_Page():
    return {"Home": "This is home page"}


@app.get("/about", tags=["General"])
def about_page():
    return {"About": "this is about page "}
