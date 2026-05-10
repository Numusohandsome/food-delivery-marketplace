import { restaurants, menuItems, fakeOrder } from "../data/mockData";

const API_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
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
    return restaurants;
  }
}

export async function getMenuByRestaurantId(restaurantId) {
  try {
    return await request(`/restaurants/${restaurantId}/menu`);
  } catch (error) {
    console.warn("Using mock menu because backend is not available.");

    return menuItems.filter(
      (item) => item.restaurantId === Number(restaurantId)
    );
  }
}

export async function createOrder(orderPayload) {
  try {
    return await request("/orders", {
      method: "POST",
      body: JSON.stringify(orderPayload),
    });
  } catch (error) {
    console.warn("Using mock order because backend is not available.");

    return {
      ...fakeOrder,
      id: Date.now(),
      items: orderPayload.items,
      total_price: orderPayload.total_price,
      totalPrice: orderPayload.total_price,
      status: "created",
    };
  }
}

export async function getOrderById(orderId) {
  try {
    return await request(`/orders/${orderId}`);
  } catch (error) {
    console.warn("Using mock order status because backend is not available.");

    const savedOrder = JSON.parse(localStorage.getItem("lastOrder"));

    if (savedOrder) {
      return savedOrder;
    }

    return {
      ...fakeOrder,
      id: orderId,
      status: "created",
    };
  }
}

export async function updateOrderStatus(orderId, status) {
  try {
    return await request(`/orders/${orderId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
  } catch (error) {
    console.warn("Using mock status update because backend is not available.");

    const savedOrder = JSON.parse(localStorage.getItem("lastOrder")) || fakeOrder;

    const updatedOrder = {
      ...savedOrder,
      id: orderId,
      status,
    };

    localStorage.setItem("lastOrder", JSON.stringify(updatedOrder));

    return updatedOrder;
  }
}