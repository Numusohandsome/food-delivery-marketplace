import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import RestaurantListPage from "./pages/RestaurantListPage";
import MenuPage from "./pages/MenuPage";
import CartPage from "./pages/CartPage";
import OrderStatusPage from "./pages/OrderStatusPage";

function App() {
  return (
    <>
      <Navbar />

      <main className="container">
        <Routes>
          <Route path="/" element={<RestaurantListPage />} />
          <Route path="/restaurants/:id/menu" element={<MenuPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/orders/:id" element={<OrderStatusPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App;