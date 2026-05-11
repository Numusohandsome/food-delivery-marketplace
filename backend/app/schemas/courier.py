from pydantic import BaseModel


class CourierOut(BaseModel):
    id: int
    full_name: str
    phone_number: str
    is_available: bool
    current_order_id: int | None = None


class CourierAvailabilityUpdate(BaseModel):
    is_available: bool
