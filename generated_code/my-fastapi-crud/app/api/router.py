from fastapi import APIRouter
from app.api.endpoints import product, auth

api_router = APIRouter()
api_router.include_router(product.router)
api_router.include_router(auth.router, tags=["authentication"])
