import requests
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException

from database.connection import products_collection
from schemas.product import Product, product_serializer

from .auth import role_required

router = APIRouter(prefix="/products", tags=["Products"])


# Sync products from DummyJSON API to MongoDB
@router.post("/sync-products")
def sync_products(admin=Depends(role_required(["admin"]))):
    response = requests.get("https://dummyjson.com/products")

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products from DummyJSON"
        )

    data = response.json()
    inserted_count, skipped_count = 0, 0

    for product in data["products"]:

        # Skip if product already exists
        existing_product = products_collection.find_one({"external_id": product["id"]})
        if existing_product:
            skipped_count += 1
            continue   

        products_collection.insert_one({
            "external_id": product["id"],
            "title": product["title"],    
            "description": product["description"], 
            "category": product["category"],
            "price": product["price"],
            "rating": product["rating"] 
        })

        inserted_count += 1

    return {
        "message": "Products synced successfully",
        "products_inserted": inserted_count,
        "products_skipped": skipped_count
    }



# Create a new product
@router.post("")
def add_Product(product: Product, admin = Depends(role_required(["admin"])), status_code=201):
    
    result = products_collection.insert_one(product.model_dump())
    return {
        "message": "product created successfully",
        "id": str(result.inserted_id),
        "product": product
    }




# Get all products
@router.get("")
def get_products():  #skip: int = 0, limit: int = 20
    products = list(products_collection.find())  #.skip(skip).limit(limit)

    return {
        "message": "Products fetched successfully",
        "count": len(products),
        "products": [product_serializer(product) for product in products]
    } 


# Get product by ID
@router.get("/{product_id}")
def get_productbyID(product_id: str):
    # print("searching ID", product_id)
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
    except InvalidId: 
        raise HTTPException(status_code=400, detail="Invalid product ID format")  from None
    
    if product:
        return {
            "product": product_serializer(product),
            "message": "product fetched successfully"
        }
    raise HTTPException(status_code=404, detail="Product not found")





# Update product by ID 
@router.put("/{product_id}") 
def update_Products(product_id: str, updated_product: Product, admin = Depends(role_required(["admin"]))):
    try:
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updated_product.model_dump(exclude_none=True)}
        )
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format") from None

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="product id not found")
    return {"message": "product updated successfully !!"}
            



# Delete product by ID
@router.delete("/{product_id}")
def delete_Product(product_id: str, admin = Depends(role_required(["admin"]))):
    try:
        resid = products_collection.delete_one({"_id": ObjectId(product_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format") from None

    if resid.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail=f"product_id {product_id} not found")



# Get products by price range
@router.get("/price/{price}")
def get_Product(price: float):
    response = requests.get("https://dummyjson.com/products")
    products = response.json() 
    print(products)
    filtered_price = []
    for prod in products:
        if price <= prod["price"] < (price + 1):
            filtered_price.append(prod)
    return filtered_price



