from pydantic import BaseModel


class Product(BaseModel):
    title: str
    price: float
    description: str | None = None
    category: str | None = None
    rating: float | None = None

# def product_serializer(product) -> dict:
#     return {
#         "id": str(product["_id"]),
#         "external_id": product["external_id"],
#         "title": product["title"],
#         "description": product.get("description", ""),
#         "category": product.get("category", ""),
#         "price": product["price"],
#         "rating": product["rating"]  # "rating": product.get("rating", 0.0)  # Default rating is 0.0 if not specified
#     }

def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "external_id": product.get("external_id"),
        "title": product["title"],
        "description": product.get("description", ""),
        "category": product.get("category", ""),
        "price": product["price"],
        "rating": product.get("rating", 0.0)
    }