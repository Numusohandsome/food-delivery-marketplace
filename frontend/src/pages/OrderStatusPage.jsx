import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

const statuses = ["created", "accepted", "preparing", "on_the_way", "delivered"];

function OrderStatusPage() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [statusIndex, setStatusIndex] = useState(0);

  useEffect(() => {
    const savedOrder = JSON.parse(localStorage.getItem("lastOrder"));

    if (savedOrder) {
      setOrder(savedOrder);
      const index = statuses.indexOf(savedOrder.status);
      setStatusIndex(index >= 0 ? index : 0);
    }
  }, []);

  useEffect(() => {
    if (!order) return;

    const interval = setInterval(() => {
      setStatusIndex((currentIndex) => {
        if (currentIndex >= statuses.length - 1) {
          clearInterval(interval);
          return currentIndex;
        }

        const nextIndex = currentIndex + 1;
        const nextStatus = statuses[nextIndex];

        const updatedOrder = {
          ...order,
          status: nextStatus,
        };

        setOrder(updatedOrder);
        localStorage.setItem("lastOrder", JSON.stringify(updatedOrder));

        return nextIndex;
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [order]);

  if (!order) {
    return (
      <section>
        <h1>Order not found</h1>
        <Link to="/">Back to restaurants</Link>
      </section>
    );
  }

  return (
    <section>
      <div className="page-header">
        <h1>Order #{id}</h1>
        <p>Live order status simulation.</p>
      </div>

      <div className="status-card">
        <h2>Current status:</h2>
        <div className={`status-badge status-${statuses[statusIndex]}`}>
          {statuses[statusIndex].replaceAll("_", " ")}
        </div>

        <div className="status-steps">
          {statuses.map((status, index) => (
            <div
              key={status}
              className={
                index <= statusIndex ? "status-step active" : "status-step"
              }
            >
              {status.replaceAll("_", " ")}
            </div>
          ))}
        </div>
      </div>

      <div className="order-summary">
        <h2>Order items</h2>

        {order.items.map((item) => (
          <div key={item.id} className="order-item">
            <span>
              {item.name} × {item.quantity}
            </span>
            <span>${(item.price * item.quantity).toFixed(2)}</span>
          </div>
        ))}

        <h3>Total: ${order.totalPrice.toFixed(2)}</h3>
      </div>

      <div className="bottom-actions">
        <Link to="/" className="primary-link">
          Create another order
        </Link>
      </div>
    </section>
  );
}

export default OrderStatusPage;