from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    restaurants = db.query(Restaurant).all()
    return restaurants


@router.get("/{restaurant_id}/menu", response_model=list[MenuItemOut])
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
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

    return menu_items
