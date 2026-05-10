from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    restaurant_id: int
    customer_id: int
    delivery_address: str
    total_price: float
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str


class OrderOut(BaseModel):
    id: int
    restaurant_id: int
    customer_id: int
    delivery_address: str
    total_price: float
    status: str
    items: List[OrderItemCreate]
