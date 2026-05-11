import { Link } from "react-router-dom";
import { ShoppingCart } from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">
      <Link to="/" className="logo">
        Food Delivery
      </Link>

      <nav>
        <Link to="/">Restaurants</Link>
        <Link to="/cart" className="cart-link">
          <ShoppingCart size={18} />
          Cart
        </Link>
      </nav>
    </header>
  );
}

export default Navbar;