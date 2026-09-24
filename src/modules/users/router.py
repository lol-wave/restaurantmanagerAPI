from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ...core.security import ALGORITHM, hash_password, verify_password, create_access_token, create_refresh_token, secret_key
from ...dependencies import get_current_user_id, get_db
from .models import UserModel
from .schemas import LoginResponse, PasswordUpdateRequest, RefreshTokenRequest, UserCreate, UserLogin, UserResponse


userrouter = APIRouter()
router = userrouter

@userrouter.post("/register/", response_model=UserResponse)
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


@userrouter.post("/login/", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    target_user = db.query(UserModel).filter(or_(UserModel.username == user.login, UserModel.email == user.login)).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Incorrect login or password!")
    if not verify_password(user.password, target_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect login or password!")

    access_token = create_access_token({"sub": str(target_user.id)})
    refresh_token = create_refresh_token({"sub": str(target_user.id)})

    return {
        "user": target_user,
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    }


@userrouter.post("/refresh/", response_model=LoginResponse)
def refresh_user_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, secret_key, algorithms=[ALGORITHM])
    except (JWTError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = int(payload["sub"])
    target_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token({"sub": str(target_user.id)})
    refresh_token = create_refresh_token({"sub": str(target_user.id)})
    return {
        "user": target_user,
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    }

@userrouter.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@userrouter.get("/me/", response_model=UserResponse)
def myself(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
	user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
	return user
	
@userrouter.patch("/password/")
def update_password(data: PasswordUpdateRequest, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    if data.new_password != data.new_password_confirm:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@userrouter.delete("/destroy/")
def delete_user(password: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@userrouter.patch("/username/")
def update_username(new_username: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user = db.query(UserModel).filter(UserModel.username == new_username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    user.username = new_username
    db.commit()
    return {"message": "Username updated successfully"}

@userrouter.patch("/email/")
def update_email(new_email: str, password: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    existing_user = db.query(UserModel).filter(UserModel.email == new_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken")
    user.email = new_email
    db.commit()
    return {"message": "Email updated successfully"}

@userrouter.patch("/phone_number/")
def update_phone_number(new_phone_number: str, password: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user.phone_number = new_phone_number
    db.commit()
    return {"message": "Phone number updated successfully"}

@userrouter.patch("/full_name/")
def update_full_name(new_full_name: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.full_name = new_full_name
    db.commit()
    return {"message": "Full name updated successfully"}

