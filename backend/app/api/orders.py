from fastapi import APIRouter, HTTPException

from app.mock_data import orders, order_status_flow
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("", response_model=OrderOut, status_code=201)
def create_order(order_data: OrderCreate):
    order_id = len(orders) + 1

    new_order = {
        "id": order_id,
        "restaurant_id": order_data.restaurant_id,
        "customer_id": order_data.customer_id,
        "delivery_address": order_data.delivery_address,
        "total_price": order_data.total_price,
        "status": "created",
        "items": order_data.items,
    }

    orders[order_id] = new_order

    return new_order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    order = orders.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, status_data: OrderStatusUpdate):
    order = orders.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if status_data.status not in order_status_flow:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed statuses: {order_status_flow}",
        )

    current_status_index = order_status_flow.index(order["status"])
    new_status_index = order_status_flow.index(status_data.status)

    if new_status_index < current_status_index:
        raise HTTPException(
            status_code=400,
            detail="Order status cannot move backwards",
        )

    order["status"] = status_data.status

    return order
