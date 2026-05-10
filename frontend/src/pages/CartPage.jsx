import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

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

  function createOrder() {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    const demoOrder = {
      id: 1,
      items: cart,
      totalPrice,
      status: "created",
      createdAt: new Date().toISOString(),
    };

    localStorage.setItem("lastOrder", JSON.stringify(demoOrder));
    localStorage.removeItem("cart");

    navigate("/orders/1");
  }

  return (
    <section>
      <div className="page-header">
        <h1>Your Cart</h1>
        <p>Review your items before creating an order.</p>
      </div>

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
              <div key={item.id} className="cart-item">
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

          <div className="cart-summary">
            <h2>Total: ${totalPrice.toFixed(2)}</h2>

            <div className="cart-actions">
              <button onClick={clearCart} className="secondary-button">
                Clear cart
              </button>

              <button onClick={createOrder} className="primary-button">
                Create order
              </button>
            </div>
          </div>
        </>
      )}
    </section>
  );
}

export default CartPage;