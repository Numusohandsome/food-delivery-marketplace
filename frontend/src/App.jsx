import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    axios
      .get("/api/restaurants")
      .then((response) => setRestaurants(response.data))
      .catch((error) => console.error("API error:", error));
  }, []);

  return (
    <main style={{ fontFamily: "Arial", padding: "40px" }}>
      <h1>Food Delivery Marketplace</h1>
      <p>Frontend is running through Docker and Nginx.</p>

      <h2>Restaurants</h2>

      {restaurants.length === 0 ? (
        <p>Loading restaurants from backend...</p>
      ) : (
        <ul>
          {restaurants.map((restaurant) => (
            <li key={restaurant.id}>
              {restaurant.name} — {restaurant.cuisine}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}