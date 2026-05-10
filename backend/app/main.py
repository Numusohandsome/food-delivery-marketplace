from fastapi import FastAPI

from app.api.router import api_router
from app.websocket.orders import router as websocket_router


app = FastAPI(
    title="Food Delivery Marketplace API",
    version="0.1.0",
    description="Backend API for food-delivery marketplace project",
)


@app.get("/", tags=["health"])
def root():
    return {
        "message": "Food Delivery Marketplace API is running",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": "backend",
    }


app.include_router(api_router, prefix="/api")
app.include_router(websocket_router)
