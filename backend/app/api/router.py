from fastapi import APIRouter

from app.api import auth, orders, restaurants, users


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(restaurants.router)
api_router.include_router(orders.router)


@api_router.get("/ping", tags=["health"])
def ping():
    return {
        "message": "pong",
    }
