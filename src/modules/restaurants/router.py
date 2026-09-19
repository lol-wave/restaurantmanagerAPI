from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...dependencies import get_db
from .models import RestaurantModel
from .schemas import RestaurantCreate, RestaurantResponse

resto_router = APIRouter()

@resto_router.post("/restaurants/", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    existing_restaurant = db.query(RestaurantModel).filter(RestaurantModel.name == restaurant.name).first()
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant with this name already exists")
    db_restourant = RestaurantModel(
        name=restaurant.name,
        description=restaurant.description,
        longitude=restaurant.longitude,
        latitude=restaurant.latitude,
        wifi_name=restaurant.wifi_name,
        wifi_password=restaurant.wifi_password,
        phone_number=restaurant.phone_number,
        email=restaurant.email,
        working_hours=restaurant.working_hours.dict() if restaurant.working_hours else None
    )
    db.add(db_restourant)
    db.commit()
    db.refresh(db_restourant)
    return db_restourant