from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Food Delivery Backend")

Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/restaurants")
def get_restaurants():
    return [
        {"id": 1, "name": "Pizza House", "cuisine": "Italian"},
        {"id": 2, "name": "Burger Point", "cuisine": "American"},
        {"id": 3, "name": "Sushi Market", "cuisine": "Japanese"},
    ]