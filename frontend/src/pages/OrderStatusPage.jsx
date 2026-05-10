import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getOrderById, updateOrderStatus } from "../api/client";
import { connectOrderStatusSocket } from "../websocket/orderSocket";

const statuses = ["created", "confirmed", "preparing", "picked_up", "delivered"];

function OrderStatusPage() {
  const params = useParams();
  const orderId = params.orderId || params.id;

  const [order, setOrder] = useState(null);
  const [currentStatus, setCurrentStatus] = useState("created");
  const [socketConnected, setSocketConnected] = useState(false);

  useEffect(() => {
    async function loadOrder() {
      const data = await getOrderById(orderId);

      setOrder(data);
      setCurrentStatus(data.status || "created");
    }

    loadOrder();
  }, [orderId]);

  useEffect(() => {
    const socket = connectOrderStatusSocket(orderId, (newStatus) => {
      setCurrentStatus(newStatus);

      setOrder((previousOrder) => {
        if (!previousOrder) {
          return previousOrder;
        }

        const updatedOrder = {
          ...previousOrder,
          status: newStatus,
        };

        localStorage.setItem("lastOrder", JSON.stringify(updatedOrder));
        return updatedOrder;
      });
    });

    if (socket) {
      socket.onopen = () => {
        setSocketConnected(true);
      };

      socket.onclose = () => {
        setSocketConnected(false);
      };
    }

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [orderId]);

  async function moveToNextStatus() {
    const currentIndex = statuses.indexOf(currentStatus);
    const nextStatus = statuses[currentIndex + 1];

    if (!nextStatus) {
      return;
    }

    const updatedOrder = await updateOrderStatus(orderId, nextStatus);

    setOrder(updatedOrder);
    setCurrentStatus(updatedOrder.status || nextStatus);
  }

  if (!order) {
    return (
      <section>
        <h1>Order not found</h1>
        <Link to="/">Back to restaurants</Link>
      </section>
    );
  }

  const orderItems = order.items || [];
  const totalPrice = order.totalPrice || order.total_price || 0;

  return (
    <section>
      <div className="page-header">
        <h1>Order Status</h1>
        <p>Live order status tracking.</p>
      </div>

      <div className="status-card">
        <p>
          <strong>Order ID:</strong> {order.id || order.order_id || orderId}
        </p>

        <p>
          <strong>Current status:</strong>{" "}
          <span className="status-label">
            {currentStatus.replaceAll("_", " ")}
          </span>
        </p>

        <p>
          <strong>WebSocket:</strong>{" "}
          {socketConnected ? "connected" : "not connected / fallback mode"}
        </p>

        <div className="status-steps">
          {statuses.map((status) => (
            <div
              key={status}
              className={
                statuses.indexOf(status) <= statuses.indexOf(currentStatus)
                  ? "status-step active"
                  : "status-step"
              }
            >
              {status.replaceAll("_", " ")}
            </div>
          ))}
        </div>

        <button
          className="primary-button"
          onClick={moveToNextStatus}
          disabled={currentStatus === "delivered"}
        >
          Move to next status
        </button>

        <h2>Order items</h2>

        {orderItems.length === 0 ? (
          <p>No order items available.</p>
        ) : (
          <div className="order-items">
            {orderItems.map((item) => (
              <div key={item.id || item.menu_item_id} className="order-item">
                <span>{item.name || `Menu item #${item.menu_item_id}`}</span>
                <span>
                  × {item.quantity}{" "}
                  {item.price ? `$${(item.price * item.quantity).toFixed(2)}` : ""}
                </span>
              </div>
            ))}
          </div>
        )}

        <h3>Total: ${Number(totalPrice).toFixed(2)}</h3>

        <Link to="/" className="primary-link">
          Create another order
        </Link>
      </div>
    </section>
  );
}

export default OrderStatusPage;