const WS_URL =
  import.meta.env.VITE_WS_BASE_URL || "ws://127.0.0.1:8000/ws";

export function connectOrderStatusSocket(orderId, onStatusUpdate) {
  if (!orderId) {
    return null;
  }

  const socketUrl = `${WS_URL}/orders/${orderId}`;

  let socket;

  try {
    socket = new WebSocket(socketUrl);
  } catch (error) {
    console.warn("WebSocket connection failed to initialize.");
    return null;
  }

  socket.onopen = () => {
    console.log("WebSocket connected:", socketUrl);
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.status) {
        onStatusUpdate(data.status);
      }
    } catch (error) {
      console.warn("Invalid WebSocket message:", event.data);
    }
  };

  socket.onerror = () => {
    console.warn("WebSocket error. Backend WebSocket may not be ready yet.");
  };

  socket.onclose = () => {
    console.log("WebSocket closed.");
  };

  return socket;
}