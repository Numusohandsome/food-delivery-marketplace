from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from app.websocket.manager import order_connection_manager


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


order_status_flow = [
    "created",
    "confirmed",
    "preparing",
    "picked_up",
    "delivered",
]


def build_order_response(order: Order, db: Session):
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return {
        "id": order.id,
        "restaurant_id": order.restaurant_id,
        "customer_id": order.customer_id,
        "courier_id": order.courier_id,
        "delivery_address": order.delivery_address,
        "total_price": float(order.total_price),
        "status": order.status,
        "items": [
            {
                "id": item.id,
                "order_id": item.order_id,
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "price": float(item.price),
            }
            for item in order_items
        ],
    }


@router.post("", response_model=OrderOut, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(User).filter(User.id == order_data.customer_id).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == order_data.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    new_order = Order(
        customer_id=order_data.customer_id,
        restaurant_id=order_data.restaurant_id,
        courier_id=None,
        delivery_address=order_data.delivery_address,
        total_price=order_data.total_price,
        status="created",
    )

    db.add(new_order)
    db.flush()

    for item_data in order_data.items:
        menu_item = (
            db.query(MenuItem)
            .filter(MenuItem.id == item_data.menu_item_id)
            .first()
        )

        if menu_item is None:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item_data.menu_item_id} not found",
            )

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            price=item_data.price,
        )

        db.add(order_item)

    status_history = OrderStatusHistory(
        order_id=new_order.id,
        old_status=None,
        new_status="created",
    )

    db.add(status_history)
    db.commit()
    db.refresh(new_order)

    return build_order_response(new_order, db)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return build_order_response(order, db)


@router.patch("/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()

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

    current_status_index = order_status_flow.index(order.status)
    new_status_index = order_status_flow.index(status_data.status)

    if new_status_index < current_status_index:
        raise HTTPException(
            status_code=400,
            detail="Order status cannot move backwards",
        )

    old_status = order.status
    order.status = status_data.status

    status_history = OrderStatusHistory(
        order_id=order.id,
        old_status=old_status,
        new_status=status_data.status,
    )

    db.add(status_history)
    db.commit()
    db.refresh(order)

    await order_connection_manager.send_order_update(
        order_id=order_id,
        message={
            "event": "order_status_updated",
            "order_id": order_id,
            "status": order.status,
        },
    )

    return build_order_response(order, db)
