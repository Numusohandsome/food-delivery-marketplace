from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserOut, status_code=201)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=user_data.password,
        role=user_data.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == login_data.email).first()

    if user is None or user.hashed_password != login_data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    fake_token = f"fake-token-for-user-{user.id}"

    return {
        "access_token": fake_token,
        "token_type": "bearer",
    }
