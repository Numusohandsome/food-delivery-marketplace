from pydantic import BaseModel


class RestaurantOut(BaseModel):
    id: int
    name: str
    description: str
    address: str
    is_open: bool


class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str
    price: float
    is_available: bool

