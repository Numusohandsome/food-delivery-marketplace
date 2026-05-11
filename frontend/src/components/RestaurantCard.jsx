import { Link } from "react-router-dom";
import { Star, Clock } from "lucide-react";

function RestaurantCard({ restaurant }) {
  return (
    <article className="restaurant-card">
      {restaurant.image && (
        <img src={restaurant.image} alt={restaurant.name} />
      )}

      <div className="restaurant-card-body">
        <h3>{restaurant.name}</h3>

        <p>{restaurant.cuisine || restaurant.description || "Restaurant"}</p>

        <div className="restaurant-meta">
          <span>
            <Star size={16} />
            {restaurant.rating || "4.5"}
          </span>

          <span>
            <Clock size={16} />
            {restaurant.deliveryTime || "25-35 min"}
          </span>
        </div>

        <Link
          to={`/restaurants/${restaurant.id}/menu`}
          className="primary-link"
          style={{ marginTop: "16px" }}
        >
          View menu
        </Link>
      </div>
    </article>
  );
}

export default RestaurantCard;