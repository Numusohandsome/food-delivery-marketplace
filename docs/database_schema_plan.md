# Database Schema Plan

## Project Overview

This project is a food-delivery marketplace application. The database is designed to store users, restaurants, menu items, customer orders, payments, courier deliveries, reviews, and order status history.

The main database is PostgreSQL. Redis is used as a cache and temporary storage layer for frequently accessed data such as restaurant menus, active restaurant lists, order status, WebSocket subscriptions, and rate limiter buckets.

---

## Main Entities

### 1. users

Stores all system users, including customers, restaurant owners, and administrators.

Main fields:

- id
- email
- full_name
- phone
- password_hash
- role
- is_active
- created_at

Purpose:

Users can place orders, write reviews, and manage restaurants depending on their role.

---

### 2. user_addresses

Stores delivery addresses for customers.

Main fields:

- id
- user_id
- address_line
- city
- latitude
- longitude
- is_default
- created_at

Relationship:

One user can have many addresses.

---

### 3. restaurant_categories

Stores restaurant categories such as Pizza, Burger, Sushi, and Uzbek Food.

Main fields:

- id
- name

Relationship:

One category can have many restaurants.

---

### 4. restaurants

Stores restaurant information.

Main fields:

- id
- category_id
- owner_id
- name
- description
- phone
- address
- is_active
- rating
- created_at

Relationship:

One restaurant has many menu items and many orders.

---

### 5. menu_items

Stores food items offered by restaurants.

Main fields:

- id
- restaurant_id
- name
- description
- price
- is_available
- created_at

Relationship:

One restaurant has many menu items.

---

### 6. orders

Stores customer orders.

Main fields:

- id
- user_id
- restaurant_id
- address_id
- status
- total_amount
- created_at
- updated_at

Relationship:

One user can place many orders.  
One restaurant can receive many orders.  
One order contains many order items.

---

### 7. order_items

Stores individual items inside an order.

Main fields:

- id
- order_id
- menu_item_id
- quantity
- unit_price

Purpose:

The unit_price is stored separately because menu item prices may change after an order is placed.

Relationship:

One order has many order items.

---

### 8. payments

Stores payment information for each order.

Main fields:

- id
- order_id
- method
- status
- amount
- created_at

Relationship:

One order has one payment.

---

### 9. couriers

Stores courier information.

Main fields:

- id
- full_name
- phone
- status
- created_at

Relationship:

One courier can handle many deliveries.

---

### 10. deliveries

Stores delivery information.

Main fields:

- id
- order_id
- courier_id
- status
- picked_up_at
- delivered_at

Relationship:

One order can have one delivery.  
One courier can have many deliveries.

---

### 11. order_status_history

Stores order status changes for tracking and auditing.

Main fields:

- id
- order_id
- old_status
- new_status
- changed_at

Purpose:

This table helps track the full lifecycle of an order from creation to delivery.

---

### 12. reviews

Stores customer reviews for restaurants.

Main fields:

- id
- user_id
- restaurant_id
- order_id
- rating
- comment
- created_at

Relationship:

One user can write many reviews.  
One restaurant can receive many reviews.  
One order can have one review.

---

## Main Relationships

| Relationship | Type |
|---|---|
| users → user_addresses | One-to-Many |
| users → orders | One-to-Many |
| users → reviews | One-to-Many |
| restaurant_categories → restaurants | One-to-Many |
| restaurants → menu_items | One-to-Many |
| restaurants → orders | One-to-Many |
| restaurants → reviews | One-to-Many |
| orders → order_items | One-to-Many |
| orders → payments | One-to-One |
| orders → deliveries | One-to-Zero-or-One |
| orders → order_status_history | One-to-Many |
| couriers → deliveries | One-to-Many |
| orders → reviews | One-to-One |

---

## Important Constraints

The database uses constraints to protect data integrity.

Examples:

- users.email must be unique
- users.phone must be unique
- menu_items.price must be greater than 0
- order_items.quantity must be greater than 0
- reviews.rating must be between 1 and 5
- orders.status must only contain valid order statuses
- payments.status must only contain valid payment statuses
- payments.method must only contain valid payment methods
- one order can have only one payment
- one order can have only one delivery
- one order can have only one review

---

## Planned Indexes

Indexes will be added for common queries.

| Query | Index |
|---|---|
| Get available menu items by restaurant | menu_items(restaurant_id, is_available) |
| Get order history by user | orders(user_id, created_at DESC) |
| Get restaurant orders by status | orders(restaurant_id, status) |
| Get order status history | order_status_history(order_id, changed_at DESC) |
| Get courier deliveries by status | deliveries(courier_id, status) |
| Search restaurants by name | GIN index with pg_trgm |

---

## Redis Cache Plan

Redis will be used for frequently accessed or temporary data.

| Key | Purpose | TTL |
|---|---|---|
| restaurant:{id}:menu | Cache restaurant menu | 300 seconds |
| restaurants:active:list | Cache active restaurant list | 120 seconds |
| order:{id}:status | Cache live order status | 30 seconds |
| rate_limit:user:{id} | Token bucket rate limiter | 60 seconds |
| ws:order:{id}:subscribers | WebSocket order subscribers | Temporary |

PostgreSQL remains the source of truth. Redis is only used for caching and fast temporary access.