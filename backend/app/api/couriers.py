from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.courier import Courier
from app.schemas.courier import CourierAvailabilityUpdate, CourierOut


router = APIRouter(
    prefix="/couriers",
    tags=["couriers"],
)


@router.get("", response_model=list[CourierOut])
def get_couriers(db: Session = Depends(get_db)):
    couriers = db.query(Courier).all()
    return couriers


@router.get("/{courier_id}", response_model=CourierOut)
def get_courier_by_id(
    courier_id: int,
    db: Session = Depends(get_db),
):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()

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
    db: Session = Depends(get_db),
):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()

    if courier is None:
        raise HTTPException(
            status_code=404,
            detail="Courier not found",
        )

    courier.is_available = availability_data.is_available

    db.commit()
    db.refresh(courier)

    return courier
