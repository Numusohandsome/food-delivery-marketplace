import { mockRestaurants, mockMenuItems, mockOrder } from "../data/mockData";

const API_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getRestaurants() {
  try {
    return await request("/restaurants");
  } catch (error) {
    console.warn("Using mock restaurants because backend is not available.");
    return mockRestaurants;
  }
}

export async function getMenuByRestaurantId(restaurantId) {
  try {
    return await request(`/restaurants/${restaurantId}/menu`);
  } catch (error) {
    console.warn("Using mock menu because backend is not available.");
    return mockMenuItems[restaurantId] || [];
  }
}

export async function createOrder(orderPayload) {
  try {
    return await request("/orders", {
      method: "POST",
      body: JSON.stringify(orderPayload)
    });
  } catch (error) {
    console.warn("Using mock order because backend is not available.");
    return {
      ...mockOrder,
      restaurant_id: orderPayload.restaurant_id,
      items: orderPayload.items,
      total_price: orderPayload.total_price
    };
  }
}

export async function getOrderById(orderId) {
  try {
    return await request(`/orders/${orderId}`);
  } catch (error) {
    console.warn("Using mock order status because backend is not available.");
    return {
      ...mockOrder,
      id: Number(orderId)
    };
  }
}