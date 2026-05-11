# Database Optimization Results

## Purpose

This document describes the indexes added to the PostgreSQL database and presents query performance measurements using `EXPLAIN ANALYZE`.

The purpose of these indexes is to optimize common queries in the food-delivery marketplace application, such as:

- retrieving available menu items for a restaurant;
- retrieving customer order history;
- filtering restaurant orders by status;
- tracking order status history;
- filtering courier deliveries;
- searching restaurants by name.

---

## Added Indexes

The indexes were added through the Alembic migration:

```text
655787a54414_add_performance_indexes.py