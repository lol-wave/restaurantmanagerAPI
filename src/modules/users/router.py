from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.security import hash_password, verify_password, create_access_token
from ...dependencies import get_current_user_id, get_db
from .models import UserModel
from .schemas import LoginResponse, UserCreate, UserLogin, UserResponse



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


@router.post("/login/", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    target_user = db.query(UserModel).filter(or_(UserModel.username == user.login, UserModel.email == user.login)).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Incorrect login or password!")
    if not verify_password(user.password, target_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect login or password!")

    access_token = create_access_token({"sub": str(target_user.id)})
    
    return {
        "user": target_user,
        "tokens": {"access_token": access_token, "token_type": "bearer"},
    }

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
    
@router.get("/me/", response_model=UserResponse)
def myself(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
	user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
	return user
	
