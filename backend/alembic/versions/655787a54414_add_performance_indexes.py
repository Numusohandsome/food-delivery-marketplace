"""add performance indexes

Revision ID: 655787a54414
Revises: 0ab3137c748d
Create Date: 2026-05-11 15:16:02.314784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '655787a54414'
down_revision: Union[str, None] = '0ab3137c748d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "idx_restaurants_category_active",
        "restaurants",
        ["category_id", "is_active"],
        unique=False,
    )

    op.create_index(
        "idx_menu_items_restaurant_available",
        "menu_items",
        ["restaurant_id", "is_available"],
        unique=False,
    )

    op.create_index(
        "idx_orders_user_created_at",
        "orders",
        ["user_id", "created_at"],
        unique=False,
    )

    op.create_index(
        "idx_orders_restaurant_status",
        "orders",
        ["restaurant_id", "status"],
        unique=False,
    )

    op.create_index(
        "idx_order_status_history_order_time",
        "order_status_history",
        ["order_id", "changed_at"],
        unique=False,
    )

    op.create_index(
        "idx_deliveries_courier_status",
        "deliveries",
        ["courier_id", "status"],
        unique=False,
    )

    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_restaurants_name_trgm
        ON restaurants
        USING gin (name gin_trgm_ops);
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_restaurants_name_trgm;")

    op.drop_index(
        "idx_deliveries_courier_status",
        table_name="deliveries",
    )

    op.drop_index(
        "idx_order_status_history_order_time",
        table_name="order_status_history",
    )

    op.drop_index(
        "idx_orders_restaurant_status",
        table_name="orders",
    )

    op.drop_index(
        "idx_orders_user_created_at",
        table_name="orders",
    )

    op.drop_index(
        "idx_menu_items_restaurant_available",
        table_name="menu_items",
    )

    op.drop_index(
        "idx_restaurants_category_active",
        table_name="restaurants",
    )
