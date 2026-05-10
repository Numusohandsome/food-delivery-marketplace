from fastapi import APIRouter, HTTPException

from app.mock_data import users
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_data: UserCreate):
    for user in users.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )

    user_id = len(users) + 1

    new_user = {
        "id": user_id,
        "full_name": user_data.full_name,
        "email": user_data.email,
        "password": user_data.password,
        "role": user_data.role,
        "is_active": True,
    }

    users[user_id] = new_user

    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(login_data: LoginRequest):
    for user in users.values():
        if (
            user["email"] == login_data.email
            and user["password"] == login_data.password
        ):
            fake_token = f"fake-token-for-user-{user['id']}"

            return {
                "access_token": fake_token,
                "token_type": "bearer",
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password",
    )
