from fastapi import APIRouter, HTTPException

from app.mock_data import couriers
from app.schemas.courier import CourierAvailabilityUpdate, CourierOut


router = APIRouter(
    prefix="/couriers",
    tags=["couriers"],
)


@router.get("", response_model=list[CourierOut])
def get_couriers():
    return list(couriers.values())


@router.get("/{courier_id}", response_model=CourierOut)
def get_courier_by_id(courier_id: int):
    courier = couriers.get(courier_id)

    if courier is None:
        raise HTTPException(
            status_code=404,
            detail="Courier not found",
        )

    return courier


@router.patch("/{courier_id}/availability", response_model=CourierOut)
def update_courier_availability(
    courier_id: int,
    availability_data: CourierAvailabilityUpdate,
):
    courier = couriers.get(courier_id)

    if courier is None:
        raise HTTPException(
            status_code=404,
            detail="Courier not found",
        )

    courier["is_available"] = availability_data.is_available

    return courier
