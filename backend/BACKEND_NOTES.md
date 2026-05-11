# Backend Core Notes

## Role

Backend Core is responsible for the FastAPI application, REST API endpoints, authentication, PostgreSQL integration, WebSocket updates, Redis caching, and the custom Token Bucket Rate Limiter.

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- WebSocket
- JWT
- Docker-ready backend structure

## Implemented REST API

### Health

- GET `/`
- GET `/health`
- GET `/api/ping`

### Auth and Users

- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/users/me`
- GET `/api/users/{user_id}`

Authentication uses password hashing and JWT token generation.

### Restaurants and Menu

- GET `/api/restaurants`
- GET `/api/restaurants/{restaurant_id}/menu`

Restaurant and menu data is stored in PostgreSQL. Redis cache is used for restaurant list and restaurant menu responses.

### Orders

- POST `/api/orders`
- GET `/api/orders/{order_id}`
- PATCH `/api/orders/{order_id}/status`

Orders are stored in PostgreSQL. The backend validates the customer, restaurant, and menu items before creating an order.

Order status flow:

1. created
2. confirmed
3. preparing
4. picked_up
5. delivered

The API prevents moving order status backwards.

### Couriers

- GET `/api/couriers`
- GET `/api/couriers/{courier_id}`
- PATCH `/api/couriers/{courier_id}/availability`

Courier data is stored in PostgreSQL.

## WebSocket Integration

The backend provides live order status updates through:

- WS `/ws/orders/{order_id}`

When an order status is updated through the REST API, the backend broadcasts the update to connected WebSocket clients.

## From-Scratch Component

The from-scratch component is a Token Bucket Rate Limiter.

It works as follows:

- Each client IP gets a bucket.
- The bucket has a limited number of tokens.
- Each HTTP request consumes one token.
- Tokens refill over time.
- If the bucket is empty, the backend returns HTTP `429 Too Many Requests`.

This protects the API from excessive requests.

## Database Layer

SQLAlchemy models were created for:

- users
- restaurants
- menu_items
- orders
- order_items
- order_status_history
- couriers

Alembic is used for database migrations.

Seed data is provided for:

- demo users
- demo restaurants
- demo menu items
- demo couriers

## Redis Cache

Redis is used to cache:

- restaurant list
- restaurant menu by restaurant id

This reduces repeated database queries for frequently requested data.

## How to Run Backend Locally

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
