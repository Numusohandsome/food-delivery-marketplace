"""seed initial food delivery data

Revision ID: 0ab3137c748d
Revises: 6102a92c59bb
Create Date: 2026-05-11 15:08:09.688627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ab3137c748d'
down_revision: Union[str, None] = '6102a92c59bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO users (id, email, full_name, phone, password_hash, role, is_active)
        VALUES
        (1, 'alice@example.com', 'Alice Johnson', '+998901111111', 'hashed_password', 'customer', true),
        (2, 'bob@example.com', 'Bob Smith', '+998902222222', 'hashed_password', 'customer', true),
        (3, 'owner1@example.com', 'Restaurant Owner One', '+998903333333', 'hashed_password', 'restaurant_owner', true),
        (4, 'owner2@example.com', 'Restaurant Owner Two', '+998904444444', 'hashed_password', 'restaurant_owner', true),
        (5, 'admin@example.com', 'System Admin', '+998905555555', 'hashed_password', 'admin', true);
    """)

    op.execute("""
        INSERT INTO user_addresses (id, user_id, address_line, city, latitude, longitude, is_default)
        VALUES
        (1, 1, 'Amir Temur Street 10', 'Tashkent', 41.311081, 69.240562, true),
        (2, 2, 'Chilanzar 15', 'Tashkent', 41.285000, 69.203000, true);
    """)

    op.execute("""
        INSERT INTO restaurant_categories (id, name)
        VALUES
        (1, 'Pizza'),
        (2, 'Burger'),
        (3, 'Sushi'),
        (4, 'Uzbek Food');
    """)

    op.execute("""
        INSERT INTO restaurants (id, category_id, owner_id, name, description, phone, address, is_active, rating)
        VALUES
        (1, 1, 3, 'Pizza House', 'Italian pizza and pasta', '+998971111111', 'Tashkent Center', true, 4.6),
        (2, 2, 3, 'Burger King Local', 'Burgers and fries', '+998972222222', 'Chilanzar', true, 4.3),
        (3, 3, 4, 'Sushi Master', 'Fresh sushi and rolls', '+998973333333', 'Yunusabad', true, 4.7),
        (4, 4, 4, 'Osh Markazi', 'Traditional Uzbek food', '+998974444444', 'Old City', true, 4.8);
    """)

    op.execute("""
        INSERT INTO menu_items (id, restaurant_id, name, description, price, is_available)
        VALUES
        (1, 1, 'Margherita Pizza', 'Classic pizza with cheese and tomato', 55000, true),
        (2, 1, 'Pepperoni Pizza', 'Pizza with pepperoni', 70000, true),
        (3, 1, 'Chicken Alfredo Pasta', 'Creamy chicken pasta', 65000, true),

        (4, 2, 'Classic Burger', 'Beef burger with cheese', 45000, true),
        (5, 2, 'Double Burger', 'Double beef patty burger', 65000, true),
        (6, 2, 'French Fries', 'Crispy potato fries', 18000, true),

        (7, 3, 'California Roll', 'Crab, avocado and rice', 60000, true),
        (8, 3, 'Philadelphia Roll', 'Salmon and cream cheese', 75000, true),
        (9, 3, 'Miso Soup', 'Traditional Japanese soup', 25000, true),

        (10, 4, 'Osh', 'Traditional Uzbek plov', 50000, true),
        (11, 4, 'Manti', 'Steamed dumplings', 40000, true),
        (12, 4, 'Shashlik', 'Grilled meat skewers', 30000, true);
    """)

    op.execute("""
        INSERT INTO couriers (id, full_name, phone, status)
        VALUES
        (1, 'Courier One', '+998991111111', 'available'),
        (2, 'Courier Two', '+998992222222', 'available'),
        (3, 'Courier Three', '+998993333333', 'offline');
    """)

    op.execute("""
        INSERT INTO orders (id, user_id, restaurant_id, address_id, status, total_amount)
        VALUES
        (1, 1, 1, 1, 'delivered', 125000),
        (2, 2, 4, 2, 'preparing', 90000),
        (3, 1, 3, 1, 'created', 135000);
    """)

    op.execute("""
        INSERT INTO order_items (id, order_id, menu_item_id, quantity, unit_price)
        VALUES
        (1, 1, 1, 1, 55000),
        (2, 1, 2, 1, 70000),

        (3, 2, 10, 1, 50000),
        (4, 2, 11, 1, 40000),

        (5, 3, 7, 1, 60000),
        (6, 3, 8, 1, 75000);
    """)

    op.execute("""
        INSERT INTO payments (id, order_id, method, status, amount)
        VALUES
        (1, 1, 'card', 'paid', 125000),
        (2, 2, 'cash', 'pending', 90000),
        (3, 3, 'wallet', 'paid', 135000);
    """)

    op.execute("""
        INSERT INTO deliveries (id, order_id, courier_id, status, picked_up_at, delivered_at)
        VALUES
        (1, 1, 1, 'delivered', CURRENT_TIMESTAMP - INTERVAL '40 minutes', CURRENT_TIMESTAMP - INTERVAL '10 minutes'),
        (2, 2, 2, 'assigned', NULL, NULL);
    """)

    op.execute("""
        INSERT INTO order_status_history (id, order_id, old_status, new_status)
        VALUES
        (1, 1, NULL, 'created'),
        (2, 1, 'created', 'confirmed'),
        (3, 1, 'confirmed', 'preparing'),
        (4, 1, 'preparing', 'ready_for_pickup'),
        (5, 1, 'ready_for_pickup', 'picked_up'),
        (6, 1, 'picked_up', 'delivered'),

        (7, 2, NULL, 'created'),
        (8, 2, 'created', 'confirmed'),
        (9, 2, 'confirmed', 'preparing'),

        (10, 3, NULL, 'created');
    """)

    op.execute("""
        INSERT INTO reviews (id, user_id, restaurant_id, order_id, rating, comment)
        VALUES
        (1, 1, 1, 1, 5, 'Great pizza and fast delivery');
    """)

    op.execute("SELECT setval('users_id_seq', 5, true);")
    op.execute("SELECT setval('user_addresses_id_seq', 2, true);")
    op.execute("SELECT setval('restaurant_categories_id_seq', 4, true);")
    op.execute("SELECT setval('restaurants_id_seq', 4, true);")
    op.execute("SELECT setval('menu_items_id_seq', 12, true);")
    op.execute("SELECT setval('couriers_id_seq', 3, true);")
    op.execute("SELECT setval('orders_id_seq', 3, true);")
    op.execute("SELECT setval('order_items_id_seq', 6, true);")
    op.execute("SELECT setval('payments_id_seq', 3, true);")
    op.execute("SELECT setval('deliveries_id_seq', 2, true);")
    op.execute("SELECT setval('order_status_history_id_seq', 10, true);")
    op.execute("SELECT setval('reviews_id_seq', 1, true);")


def downgrade() -> None:
    op.execute("DELETE FROM reviews;")
    op.execute("DELETE FROM order_status_history;")
    op.execute("DELETE FROM deliveries;")
    op.execute("DELETE FROM payments;")
    op.execute("DELETE FROM order_items;")
    op.execute("DELETE FROM orders;")
    op.execute("DELETE FROM couriers;")
    op.execute("DELETE FROM menu_items;")
    op.execute("DELETE FROM restaurants;")
    op.execute("DELETE FROM restaurant_categories;")
    op.execute("DELETE FROM user_addresses;")
    op.execute("DELETE FROM users;")
