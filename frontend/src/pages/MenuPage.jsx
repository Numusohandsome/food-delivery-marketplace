import { useParams, Link } from "react-router-dom";
import { restaurants, menuItems } from "../data/mockData";
import MenuItemCard from "../components/MenuItemCard";

function MenuPage() {
  const { id } = useParams();
  const restaurantId = Number(id);

  const restaurant = restaurants.find((r) => r.id === restaurantId);
  const items = menuItems.filter((item) => item.restaurantId === restaurantId);

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

  if (!restaurant) {
    return (
      <section>
        <h1>Restaurant not found</h1>
        <Link to="/">Back to restaurants</Link>
      </section>
    );
  }

  return (
    <section>
      <div className="page-header">
        <h1>{restaurant.name}</h1>
        <p>
          {restaurant.cuisine} • {restaurant.deliveryTime}
        </p>
      </div>

      <div className="menu-list">
        {items.map((item) => (
          <MenuItemCard key={item.id} item={item} onAddToCart={addToCart} />
        ))}
      </div>

      <div className="bottom-actions">
        <Link to="/cart" className="primary-link">
          Go to cart
        </Link>
      </div>
    </section>
  );
}

export default MenuPage;