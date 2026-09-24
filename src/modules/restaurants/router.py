from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...modules.users.models import UserModel
from ...dependencies import get_current_user_id, get_db
from .models import RestaurantModel
from .schemas import RestaurantCreate, RestaurantResponse
from ..menus.models import MenuModel
from ..menus.schemas import MenuResponse

resto_router = APIRouter()

@resto_router.post("/restaurants/", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    existing_restaurant = db.query(RestaurantModel).filter(RestaurantModel.name == restaurant.name).first()
    
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant with this name already exists")
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()

    db_restourant = RestaurantModel(
        name=restaurant.name,
        description=restaurant.description,
        longitude=restaurant.longitude,
        latitude=restaurant.latitude,
        wifi_name=restaurant.wifi_name,
        wifi_password=restaurant.wifi_password,
        phone_number=restaurant.phone_number,
        email=restaurant.email,
        working_hours={},
        owner_id=current_user_id,
        owner=user
    )

    db.add(db_restourant)
    db.commit()
    db.refresh(db_restourant)
    return db_restourant

@resto_router.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@resto_router.get("/restaurants/{restaurant_id}/menu", response_model=MenuResponse)
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuModel).filter(MenuModel.restaurant_id == restaurant_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

