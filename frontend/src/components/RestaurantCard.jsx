import { Link } from "react-router-dom";
import { Star, Clock } from "lucide-react";

function RestaurantCard({ restaurant }) {
  return (
    <Link to={`/restaurants/${restaurant.id}`} className="restaurant-card">
      <img src={restaurant.image} alt={restaurant.name} />

      <div className="restaurant-card-body">
        <h3>{restaurant.name}</h3>
        <p>{restaurant.cuisine}</p>

        <div className="restaurant-meta">
          <span>
            <Star size={16} /> {restaurant.rating}
          </span>
          <span>
            <Clock size={16} /> {restaurant.deliveryTime}
          </span>
        </div>
      </div>
    </Link>
  );
}

export default RestaurantCard;