import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createOrder } from "../api/client";

function CartPage() {
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const savedCart = JSON.parse(localStorage.getItem("cart")) || [];
    setCart(savedCart);
  }, []);

  const totalPrice = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  function removeItem(itemId) {
    const updatedCart = cart.filter((item) => item.id !== itemId);
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  }

  function clearCart() {
    setCart([]);
    localStorage.removeItem("cart");
  }

  async function handleCreateOrder() {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    const orderPayload = {
      restaurant_id: cart[0]?.restaurantId || cart[0]?.restaurant_id || 1,
      customer_id: 1,
      delivery_address: "Demo address, Tashkent",
      total_price: Number(totalPrice.toFixed(2)),
      items: cart.map((item) => ({
        menu_item_id: item.id,
        quantity: item.quantity,
        name: item.name,
        price: item.price,
      })),
    };

    const createdOrder = await createOrder(orderPayload);

    const normalizedOrder = {
      ...createdOrder,
      id: createdOrder.id || createdOrder.order_id || Date.now(),
      items: cart,
      totalPrice:
        createdOrder.totalPrice ||
        createdOrder.total_price ||
        Number(totalPrice.toFixed(2)),
      status: createdOrder.status || "created",
    };

    localStorage.setItem("lastOrder", JSON.stringify(normalizedOrder));
    localStorage.removeItem("cart");

    navigate(`/orders/${normalizedOrder.id}`);
  }

  return (
    <section>
      <h1>Your Cart</h1>
      <p>Review your items before creating an order.</p>

      {cart.length === 0 ? (
        <div className="empty-state">
          <p>Your cart is empty.</p>
          <Link to="/" className="primary-link">
            Go to restaurants
          </Link>
        </div>
      ) : (
        <>
          <div className="cart-list">
            {cart.map((item) => (
              <div className="cart-item" key={item.id}>
                <div>
                  <h3>{item.name}</h3>
                  <p>
                    ${item.price.toFixed(2)} × {item.quantity}
                  </p>
                </div>

                <button onClick={() => removeItem(item.id)}>Remove</button>
              </div>
            ))}
          </div>

          <h2>Total: ${totalPrice.toFixed(2)}</h2>

          <div className="bottom-actions">
            <button onClick={clearCart}>Clear cart</button>
            <button onClick={handleCreateOrder} className="primary-button">
              Create order
            </button>
          </div>
        </>
      )}
    </section>
  );
}

export default CartPage;