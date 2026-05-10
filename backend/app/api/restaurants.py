from fastapi import APIRouter, HTTPException

from app.mock_data import restaurants, menu_items
from app.schemas.restaurant import RestaurantOut, MenuItemOut


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


@router.get("", response_model=list[RestaurantOut])
def get_restaurants():
    return restaurants


@router.get("/{restaurant_id}/menu", response_model=list[MenuItemOut])
def get_restaurant_menu(restaurant_id: int):
    restaurant_exists = any(
        restaurant["id"] == restaurant_id for restaurant in restaurants
    )

    if not restaurant_exists:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    restaurant_menu = [
        item for item in menu_items if item["restaurant_id"] == restaurant_id
    ]

    return restaurant_menu
