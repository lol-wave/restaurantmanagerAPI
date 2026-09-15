from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import hash_password
from ...database import get_db
from ...dependencies import get_current_user_id
from .models import UserModel
from .schemas import User, UserCreate, UserLogin, UserResponse

router = APIRouter()

@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter((UserModel.username == user.username) | (UserModel.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/", response_model=UserResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    pass

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user