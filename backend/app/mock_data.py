restaurants = [
    {
        "id": 1,
        "name": "Pizza House",
        "description": "Italian pizza and pasta",
        "address": "Amir Temur Street, Tashkent",
        "is_open": True,
    },
    {
        "id": 2,
        "name": "Burger City",
        "description": "Burgers, fries and drinks",
        "address": "Chilanzar, Tashkent",
        "is_open": True,
    },
]

menu_items = [
    {
        "id": 1,
        "restaurant_id": 1,
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce and mozzarella",
        "price": 9.99,
        "is_available": True,
    },
    {
        "id": 2,
        "restaurant_id": 1,
        "name": "Pepperoni Pizza",
        "description": "Pizza with pepperoni and cheese",
        "price": 11.99,
        "is_available": True,
    },
    {
        "id": 3,
        "restaurant_id": 2,
        "name": "Classic Burger",
        "description": "Beef burger with cheese and vegetables",
        "price": 7.99,
        "is_available": True,
    },
]

orders = {}

order_status_flow = [
    "created",
    "confirmed",
    "preparing",
    "picked_up",
    "delivered",
]


users = {
    1: {
        "id": 1,
        "full_name": "Demo Customer",
        "email": "customer@example.com",
        "password": "password123",
        "role": "customer",
        "is_active": True,
    },
    2: {
        "id": 2,
        "full_name": "Demo Restaurant Owner",
        "email": "owner@example.com",
        "password": "password123",
        "role": "restaurant_owner",
        "is_active": True,
    },
    3: {
        "id": 3,
        "full_name": "Demo Courier",
        "email": "courier@example.com",
        "password": "password123",
        "role": "courier",
        "is_active": True,
    },
}


couriers = {
    1: {
        "id": 1,
        "full_name": "Demo Courier One",
        "phone_number": "+998901112233",
        "is_available": True,
        "current_order_id": None,
    },
    2: {
        "id": 2,
        "full_name": "Demo Courier Two",
        "phone_number": "+998902223344",
        "is_available": False,
        "current_order_id": 1,
    },
}
