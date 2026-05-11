# Redis Cache Design

## Purpose

Redis is used as a cache and temporary storage layer in the food-delivery marketplace application.

PostgreSQL is the main source of truth for persistent relational data, such as users, restaurants, menu items, orders, payments, deliveries, and reviews.

Redis is used for data that is frequently accessed, temporary, or needs very fast read/write operations.

---

## Why Redis Is Used

Redis is used for the following reasons:

- to reduce repeated PostgreSQL queries;
- to speed up frequently accessed API responses;
- to store short-lived order tracking data;
- to support WebSocket order subscriptions;
- to support the token bucket rate limiter;
- to improve scalability under high request load.

Redis does not replace PostgreSQL. It only improves performance for selected use cases.

---

## Cached Data

### 1. Restaurant Menu Cache

Restaurant menus are read frequently by customers. Instead of querying PostgreSQL every time, the menu can be cached in Redis.

Example key:

```text
restaurant:{restaurant_id}:menu