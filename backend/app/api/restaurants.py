import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.redis_client import redis_client
from app.db.session import get_db
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.schemas.restaurant import MenuItemOut, RestaurantOut


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


@router.get("", response_model=list[RestaurantOut])
def get_restaurants(db: Session = Depends(get_db)):
    cache_key = "restaurants:list"

    cached_restaurants = redis_client.get(cache_key)

    if cached_restaurants is not None:
        return json.loads(cached_restaurants)

    restaurants = db.query(Restaurant).all()

    result = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "address": restaurant.address,
            "category": restaurant.category,
            "is_open": restaurant.is_open,
        }
        for restaurant in restaurants
    ]

    redis_client.setex(
        cache_key,
        60,
        json.dumps(result),
    )

    return result


@router.get("/{restaurant_id}/menu", response_model=list[MenuItemOut])
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    cache_key = f"restaurants:{restaurant_id}:menu"

    cached_menu = redis_client.get(cache_key)

    if cached_menu is not None:
        return json.loads(cached_menu)

    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    menu_items = (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .all()
    )

    result = [
        {
            "id": item.id,
            "restaurant_id": item.restaurant_id,
            "name": item.name,
            "description": item.description,
            "price": float(item.price),
            "is_available": item.is_available,
        }
        for item in menu_items
    ]

    redis_client.setex(
        cache_key,
        60,
        json.dumps(result),
    )

    return result
