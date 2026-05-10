import { restaurants } from "../data/mockData";
import RestaurantCard from "../components/RestaurantCard";

function RestaurantListPage() {
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