from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="customer")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    addresses = relationship("UserAddress", back_populates="user")
    orders = relationship("Order", back_populates="user")
    restaurants = relationship("Restaurant", back_populates="owner")
    reviews = relationship("Review", back_populates="user")

    __table_args__ = (
        CheckConstraint(
            "role IN ('customer', 'restaurant_owner', 'admin')",
            name="chk_users_role",
        ),
    )


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    address_line: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude = mapped_column(Numeric(9, 6))
    longitude = mapped_column(Numeric(9, 6))
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="addresses")


class RestaurantCategory(Base):
    __tablename__ = "restaurant_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    restaurants = relationship("Restaurant", back_populates="category")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("restaurant_categories.id", ondelete="SET NULL")
    )
    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    rating = mapped_column(Numeric(2, 1), nullable=False, default=0.0)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    category = relationship("RestaurantCategory", back_populates="restaurants")
    owner = relationship("User", back_populates="restaurants")
    menu_items = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")

    __table_args__ = (
        CheckConstraint(
            "rating >= 0 AND rating <= 5",
            name="chk_restaurant_rating",
        ),
    )


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price = mapped_column(Numeric(10, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")

    __table_args__ = (
        CheckConstraint("price > 0", name="chk_menu_item_price"),
        UniqueConstraint(
            "restaurant_id",
            "name",
            name="uq_menu_item_per_restaurant",
        ),
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id", ondelete="RESTRICT"),
        nullable=False,
    )
    address_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_addresses.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="created")
    total_amount = mapped_column(Numeric(10, 2), nullable=False, default=0)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
    delivery = relationship("Delivery", back_populates="order", uselist=False)
    status_history = relationship("OrderStatusHistory", back_populates="order")
    review = relationship("Review", back_populates="order", uselist=False)

    __table_args__ = (
        CheckConstraint(
            "status IN ('created', 'confirmed', 'preparing', 'ready_for_pickup', 'picked_up', 'delivered', 'cancelled')",
            name="chk_order_status",
        ),
        CheckConstraint("total_amount >= 0", name="chk_order_total"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price = mapped_column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_order_item_quantity"),
        CheckConstraint("unit_price > 0", name="chk_order_item_price"),
        UniqueConstraint("order_id", "menu_item_id", name="uq_order_menu_item"),
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    method: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    amount = mapped_column(Numeric(10, 2), nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment")

    __table_args__ = (
        CheckConstraint(
            "method IN ('cash', 'card', 'wallet')",
            name="chk_payment_method",
        ),
        CheckConstraint(
            "status IN ('pending', 'paid', 'failed', 'refunded')",
            name="chk_payment_status",
        ),
        CheckConstraint("amount >= 0", name="chk_payment_amount"),
    )


class Courier(Base):
    __tablename__ = "couriers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="available")
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    deliveries = relationship("Delivery", back_populates="courier")

    __table_args__ = (
        CheckConstraint(
            "status IN ('available', 'busy', 'offline')",
            name="chk_courier_status",
        ),
    )


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    courier_id: Mapped[int | None] = mapped_column(
        ForeignKey("couriers.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="assigned")
    picked_up_at = mapped_column(DateTime)
    delivered_at = mapped_column(DateTime)

    order = relationship("Order", back_populates="delivery")
    courier = relationship("Courier", back_populates="deliveries")

    __table_args__ = (
        CheckConstraint(
            "status IN ('assigned', 'picked_up', 'delivered', 'failed')",
            name="chk_delivery_status",
        ),
    )


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    old_status: Mapped[str | None] = mapped_column(String(30))
    new_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="status_history")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    order = relationship("Order", back_populates="review")

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="chk_review_rating"),
    )