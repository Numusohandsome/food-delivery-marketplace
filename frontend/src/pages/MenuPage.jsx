import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import MenuItemCard from "../components/MenuItemCard";
import { getRestaurants, getMenuByRestaurantId } from "../api/client";

function MenuPage() {
  const { id } = useParams();
  const restaurantId = Number(id);

  const [restaurant, setRestaurant] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMenuPage() {
      try {
        const restaurantList = await getRestaurants();

        const selectedRestaurant = restaurantList.find(
          (item) => Number(item.id) === restaurantId
        );

        const menu = await getMenuByRestaurantId(restaurantId);

        setRestaurant(selectedRestaurant);
        setItems(menu);
      } finally {
        setLoading(false);
      }
    }

    loadMenuPage();
  }, [restaurantId]);

  function addToCart(item) {
    const currentCart = JSON.parse(localStorage.getItem("cart")) || [];

    const existingItem = currentCart.find((cartItem) => cartItem.id === item.id);

    let updatedCart;

    if (existingItem) {
      updatedCart = currentCart.map((cartItem) =>
        cartItem.id === item.id
          ? { ...cartItem, quantity: cartItem.quantity + 1 }
          : cartItem
      );
    } else {
      updatedCart = [...currentCart, { ...item, quantity: 1 }];
    }

    localStorage.setItem("cart", JSON.stringify(updatedCart));
    alert(`${item.name} added to cart`);
  }

  if (loading) {
    return (
      <section>
        <h1>Loading menu...</h1>
      </section>
    );
  }

  if (!restaurant) {
    return (
      <section>
        <h1>Restaurant not found</h1>
        <Link to="/" className="primary-link">
          Back to restaurants
        </Link>
      </section>
    );
  }

  return (
    <section>
      <div className="page-header">
        <h1>{restaurant.name}</h1>
        <p>
          {restaurant.cuisine || restaurant.description || "Restaurant"} •{" "}
          {restaurant.deliveryTime || "25-35 min"}
        </p>
      </div>

      {items.length === 0 ? (
        <p>No menu items available.</p>
      ) : (
        <div className="menu-list">
          {items.map((item) => (
            <MenuItemCard key={item.id} item={item} onAddToCart={addToCart} />
          ))}
        </div>
      )}

      <div className="bottom-actions">
        <Link to="/cart" className="primary-link">
          Go to cart
        </Link>
      </div>
    </section>
  );
}

export default MenuPage;