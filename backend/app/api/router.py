from fastapi import APIRouter

from app.api import restaurants, orders


api_router = APIRouter()

api_router.include_router(restaurants.router)
api_router.include_router(orders.router)


@api_router.get("/ping", tags=["health"])
def ping():
    return {
        "message": "pong",
    }
