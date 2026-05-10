export const restaurants = [
  {
    id: 1,
    name: "Pizza House",
    cuisine: "Italian",
    rating: 4.7,
    deliveryTime: "25-35 min",
    image:
      "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
  },
  {
    id: 2,
    name: "Sushi Market",
    cuisine: "Japanese",
    rating: 4.8,
    deliveryTime: "30-40 min",
    image:
      "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800",
  },
  {
    id: 3,
    name: "Burger Point",
    cuisine: "American",
    rating: 4.5,
    deliveryTime: "20-30 min",
    image:
      "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
  },
];

export const menuItems = [
  {
    id: 1,
    restaurantId: 1,
    name: "Margherita Pizza",
    description: "Classic pizza with tomato sauce, mozzarella, and basil.",
    price: 8.99,
  },
  {
    id: 2,
    restaurantId: 1,
    name: "Pepperoni Pizza",
    description: "Pizza with mozzarella cheese and pepperoni.",
    price: 10.99,
  },
  {
    id: 3,
    restaurantId: 2,
    name: "Salmon Sushi Set",
    description: "Fresh salmon sushi with soy sauce and wasabi.",
    price: 12.5,
  },
  {
    id: 4,
    restaurantId: 2,
    name: "California Roll",
    description: "Crab, avocado, cucumber, and rice roll.",
    price: 9.5,
  },
  {
    id: 5,
    restaurantId: 3,
    name: "Classic Burger",
    description: "Beef patty, cheese, lettuce, tomato, and sauce.",
    price: 7.99,
  },
  {
    id: 6,
    restaurantId: 3,
    name: "Double Cheese Burger",
    description: "Double beef patty with cheddar cheese.",
    price: 10.99,
  },
];

export const fakeOrder = {
  id: 1,
  status: "created",
  customerName: "Demo Customer",
  restaurantName: "Pizza House",
  totalPrice: 19.98,
};