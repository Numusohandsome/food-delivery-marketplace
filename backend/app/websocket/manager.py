from fastapi import WebSocket


class OrderConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, order_id: int, websocket: WebSocket):
        await websocket.accept()

        if order_id not in self.active_connections:
            self.active_connections[order_id] = []

        self.active_connections[order_id].append(websocket)

    def disconnect(self, order_id: int, websocket: WebSocket):
        connections = self.active_connections.get(order_id)

        if connections is None:
            return

        if websocket in connections:
            connections.remove(websocket)

        if len(connections) == 0:
            del self.active_connections[order_id]

    async def send_order_update(self, order_id: int, message: dict):
        connections = self.active_connections.get(order_id, [])

        for websocket in connections:
            await websocket.send_json(message)


order_connection_manager = OrderConnectionManager()

