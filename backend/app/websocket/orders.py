import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.mock_data import orders


router = APIRouter(
    tags=["websocket"],
)


@router.websocket("/ws/orders/{order_id}")
async def order_status_websocket(websocket: WebSocket, order_id: int):
    await websocket.accept()

    try:
        while True:
            order = orders.get(order_id)

            if order is None:
                await websocket.send_json(
                    {
                        "error": "Order not found",
                        "order_id": order_id,
                    }
                )
            else:
                await websocket.send_json(
                    {
                        "order_id": order_id,
                        "status": order["status"],
                    }
                )

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for order_id={order_id}")
