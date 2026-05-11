from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

api_router = APIRouter()

ORDER_STATUSES = ["created", "confirmed", "preparing", "picked_up", "delivered"]

restaurants = [
    {
        "id": 1,
        "name": "Tashkent Plov Center",
        "cuisine": "Uzbek",
        "rating": 4.8,
        "delivery_time_minutes": 35,
    },
    {
        "id": 2,
        "name": "Pizza Roma",
        "cuisine": "Italian",
        "rating": 4.5,
        "delivery_time_minutes": 30,
    },
    {
        "id": 3,
        "name": "Burger House",
        "cuisine": "Fast Food",
        "rating": 4.3,
        "delivery_time_minutes": 25,
    },
]

menu_items = [
    {
        "id": 101,
        "restaurant_id": 1,
        "name": "Chicken Plov",
        "description": "Traditional Uzbek plov with chicken",
        "price": 19.98,
        "is_available": True,
    },
    {
        "id": 102,
        "restaurant_id": 1,
        "name": "Achichuk Salad",
        "description": "Fresh tomato and onion salad",
        "price": 4.50,
        "is_available": True,
    },
    {
        "id": 201,
        "restaurant_id": 2,
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato and mozzarella",
        "price": 8.99,
        "is_available": True,
    },
    {
        "id": 202,
        "restaurant_id": 2,
        "name": "Pepperoni Pizza",
        "description": "Pizza with pepperoni and cheese",
        "price": 10.99,
        "is_available": True,
    },
    {
        "id": 301,
        "restaurant_id": 3,
        "name": "Cheeseburger",
        "description": "Beef burger with cheese",
        "price": 8.99,
        "is_available": True,
    },
]

orders = {}
next_order_id = 1001


class CreateOrderItem(BaseModel):
    menu_item_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    restaurant_id: int
    customer_id: int = 1
    delivery_address: str = "Demo address, Tashkent"
    total_price: float
    items: List[CreateOrderItem]


class OrderStatusUpdate(BaseModel):
    status: str


@api_router.get("/restaurants")
def get_restaurants():
    return restaurants


@api_router.get("/restaurants/{restaurant_id}/menu")
def get_restaurant_menu(restaurant_id: int):
    restaurant_exists = any(
        restaurant["id"] == restaurant_id for restaurant in restaurants
    )

    if not restaurant_exists:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return [
        item
        for item in menu_items
        if item["restaurant_id"] == restaurant_id and item["is_available"]
    ]


@api_router.post("/orders")
async def create_order(payload: CreateOrderRequest):
    global next_order_id

    restaurant_exists = any(
        restaurant["id"] == payload.restaurant_id for restaurant in restaurants
    )

    if not restaurant_exists:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    order_id = next_order_id
    next_order_id += 1

    order = {
        "id": order_id,
        "restaurant_id": payload.restaurant_id,
        "customer_id": payload.customer_id,
        "delivery_address": payload.delivery_address,
        "total_price": payload.total_price,
        "status": "created",
        "items": [item.model_dump() for item in payload.items],
    }

    orders[order_id] = order
    return order


@api_router.get("/orders/{order_id}")
def get_order(order_id: int):
    order = orders.get(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@api_router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, payload: OrderStatusUpdate):
    order = orders.get(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.status not in ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid order status")

    order["status"] = payload.status
    orders[order_id] = order

    return order
