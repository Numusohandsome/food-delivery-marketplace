from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

active_connections: dict[int, list[WebSocket]] = {}


@router.websocket("/ws/orders/{order_id}")
async def websocket_order_status(websocket: WebSocket, order_id: int):
    await websocket.accept()

    if order_id not in active_connections:
        active_connections[order_id] = []

    active_connections[order_id].append(websocket)

    await websocket.send_json(
        {
            "order_id": order_id,
            "status": "connected",
        }
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[order_id].remove(websocket)

        if not active_connections[order_id]:
            del active_connections[order_id]


async def broadcast_order_status(order_id: int, status: str):
    message = {
        "order_id": order_id,
        "status": status,
    }

    connections = active_connections.get(order_id, [])

    for websocket in connections:
        await websocket.send_json(message)
