from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserOut)
def get_current_user(db: Session = Depends(get_db)):
    """
    Temporary endpoint.

    In the final version, this will use JWT authentication.
    For now, it returns demo user with id=1.
    """
    user = db.query(User).filter(User.id == 1).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Demo user not found",
        )

    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
