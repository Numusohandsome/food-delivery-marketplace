# ER Diagram

This ER diagram represents the main entities and relationships of the food-delivery marketplace database.

```mermaid
erDiagram
    USERS ||--o{ USER_ADDRESSES : has
    USERS ||--o{ ORDERS : places
    USERS ||--o{ REVIEWS : writes

    RESTAURANT_CATEGORIES ||--o{ RESTAURANTS : categorizes
    USERS ||--o{ RESTAURANTS : owns

    RESTAURANTS ||--o{ MENU_ITEMS : offers
    RESTAURANTS ||--o{ ORDERS : receives
    RESTAURANTS ||--o{ REVIEWS : receives

    ORDERS ||--o{ ORDER_ITEMS : contains
    MENU_ITEMS ||--o{ ORDER_ITEMS : included_in

    ORDERS ||--|| PAYMENTS : has
    ORDERS ||--o| DELIVERIES : has
    ORDERS ||--o{ ORDER_STATUS_HISTORY : tracks
    ORDERS ||--o| REVIEWS : reviewed_by

    COURIERS ||--o{ DELIVERIES : handles

    USERS {
        int id PK
        varchar email UK
        varchar full_name
        varchar phone UK
        varchar password_hash
        varchar role
        boolean is_active
        timestamp created_at
    }

    USER_ADDRESSES {
        int id PK
        int user_id FK
        text address_line
        varchar city
        numeric latitude
        numeric longitude
        boolean is_default
        timestamp created_at
    }

    RESTAURANT_CATEGORIES {
        int id PK
        varchar name UK
    }

    RESTAURANTS {
        int id PK
        int category_id FK
        int owner_id FK
        varchar name
        text description
        varchar phone
        text address
        boolean is_active
        numeric rating
        timestamp created_at
    }

    MENU_ITEMS {
        int id PK
        int restaurant_id FK
        varchar name
        text description
        numeric price
        boolean is_available
        timestamp created_at
    }

    ORDERS {
        int id PK
        int user_id FK
        int restaurant_id FK
        int address_id FK
        varchar status
        numeric total_amount
        timestamp created_at
        timestamp updated_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int menu_item_id FK
        int quantity
        numeric unit_price
    }

    PAYMENTS {
        int id PK
        int order_id FK
        varchar method
        varchar status
        numeric amount
        timestamp created_at
    }

    COURIERS {
        int id PK
        varchar full_name
        varchar phone UK
        varchar status
        timestamp created_at
    }

    DELIVERIES {
        int id PK
        int order_id FK
        int courier_id FK
        varchar status
        timestamp picked_up_at
        timestamp delivered_at
    }

    ORDER_STATUS_HISTORY {
        int id PK
        int order_id FK
        varchar old_status
        varchar new_status
        timestamp changed_at
    }

    REVIEWS {
        int id PK
        int user_id FK
        int restaurant_id FK
        int order_id FK
        int rating
        text comment
        timestamp created_at
    }
```

## Relationship Explanation

| Relationship | Type | Explanation |
|---|---|---|
| users → user_addresses | One-to-Many | One customer can store multiple delivery addresses. |
| users → orders | One-to-Many | One customer can place multiple orders. |
| users → restaurants | One-to-Many | One restaurant owner can manage multiple restaurants. |
| restaurant_categories → restaurants | One-to-Many | One category can include many restaurants. |
| restaurants → menu_items | One-to-Many | One restaurant can offer many menu items. |
| restaurants → orders | One-to-Many | One restaurant can receive many orders. |
| orders → order_items | One-to-Many | One order can contain multiple food items. |
| menu_items → order_items | One-to-Many | One menu item can appear in many orders. |
| orders → payments | One-to-One | One order has one payment record. |
| orders → deliveries | One-to-Zero-or-One | One order may have one delivery record. |
| couriers → deliveries | One-to-Many | One courier can handle many deliveries. |
| orders → order_status_history | One-to-Many | One order can have many status updates. |
| users → reviews | One-to-Many | One user can write many reviews. |
| restaurants → reviews | One-to-Many | One restaurant can receive many reviews. |
| orders → reviews | One-to-Zero-or-One | One completed order can have one review. |

## Notes

The design separates orders and order items to support multiple menu items in a single order.  
The payment, delivery, and review tables are separated from orders to keep the schema normalized.  
The order_status_history table is used for tracking and auditing status changes during the order lifecycle.