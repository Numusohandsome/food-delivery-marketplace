import { useEffect, useState } from "react";
import RestaurantCard from "../components/RestaurantCard";
import { getRestaurants } from "../api/client";

function RestaurantListPage() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    async function loadRestaurants() {
      const data = await getRestaurants();
      setRestaurants(data);
    }

    loadRestaurants();
  }, []);

  return (
    <section>
      <div className="page-header">
        <h1>Restaurants</h1>
        <p>Choose a restaurant and start your order.</p>
      </div>

      <div className="restaurant-grid">
        {restaurants.map((restaurant) => (
          <RestaurantCard key={restaurant.id} restaurant={restaurant} />
        ))}
      </div>
    </section>
  );
}

export default RestaurantListPage;