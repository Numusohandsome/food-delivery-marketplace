from app.db.session import SessionLocal
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.courier import Courier
from app.core.security import get_password_hash

def seed_users(db):
    existing_user = db.query(User).filter(User.email == "customer@example.com").first()

    if existing_user:
        return

    users = [
        User(
            full_name="Demo Customer",
            email="customer@example.com",
	hashed_password=get_password_hash("password123"),
            role="customer",
            is_active=True,
        ),
        User(
            full_name="Demo Restaurant Owner",
            email="owner@example.com",
            hashed_password=get_password_hash("password123"),
            role="restaurant_owner",
            is_active=True,
        ),
        User(
            full_name="Demo Courier",
            email="courier@example.com",
            hashed_password=get_password_hash("password123"),
            role="courier",
            is_active=True,
        ),
    ]

    db.add_all(users)


def seed_restaurants(db):
    existing_restaurant = db.query(Restaurant).filter(Restaurant.name == "Pizza House").first()

    if existing_restaurant:
        return

    restaurants = [
        Restaurant(
            name="Pizza House",
            description="Italian pizza and pasta",
            address="Amir Temur Street, Tashkent",
            category="Pizza",
            is_open=True,
        ),
        Restaurant(
            name="Burger City",
            description="Burgers, fries and drinks",
            address="Chilanzar, Tashkent",
            category="Burgers",
            is_open=True,
        ),
    ]

    db.add_all(restaurants)
    db.flush()

    pizza_house = restaurants[0]
    burger_city = restaurants[1]

    menu_items = [
        MenuItem(
            restaurant_id=pizza_house.id,
            name="Margherita Pizza",
            description="Classic pizza with tomato sauce and mozzarella",
            price=9.99,
            is_available=True,
        ),
        MenuItem(
            restaurant_id=pizza_house.id,
            name="Pepperoni Pizza",
            description="Pizza with pepperoni and cheese",
            price=11.99,
            is_available=True,
        ),
        MenuItem(
            restaurant_id=burger_city.id,
            name="Classic Burger",
            description="Beef burger with cheese and vegetables",
            price=7.99,
            is_available=True,
        ),
    ]

    db.add_all(menu_items)


def seed_couriers(db):
    existing_courier = db.query(Courier).filter(Courier.phone_number == "+998901112233").first()

    if existing_courier:
        return

    couriers = [
        Courier(
            full_name="Demo Courier One",
            phone_number="+998901112233",
            is_available=True,
            current_order_id=None,
        ),
        Courier(
            full_name="Demo Courier Two",
            phone_number="+998902223344",
            is_available=True,
            current_order_id=None,
        ),
    ]

    db.add_all(couriers)


def main():
    db = SessionLocal()

    try:
        seed_users(db)
        seed_restaurants(db)
        seed_couriers(db)

        db.commit()
        print("Seed data inserted successfully")

    except Exception as error:
        db.rollback()
        print(f"Seed data failed: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()

