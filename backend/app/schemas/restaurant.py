from pydantic import BaseModel


class RestaurantOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    address: str
    category: str | None = None
    is_open: bool


class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str | None = None
    price: float
    is_available: bool
