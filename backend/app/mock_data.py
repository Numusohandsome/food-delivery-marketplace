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
