from fastapi import APIRouter, HTTPException

from app.mock_data import users
from app.schemas.user import UserOut


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserOut)
def get_current_user():
    """
    Temporary endpoint.

    In the final version, this will use JWT authentication.
    For now, it returns demo user with id=1.
    """
    return users[1]


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int):
    user = users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
