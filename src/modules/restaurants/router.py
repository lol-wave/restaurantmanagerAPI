from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from .models import RestaurantModel
from .schemas import RestaurantBase, RestaurantCreate, RestaurantResponse

router = APIRouter()

@router.post("/new_resto/", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):

    existing_restaurant = db.query(RestaurantModel).filter(RestaurantModel.name == restaurant.name).first()
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant with this name already exists")

    
    new_restaurant = RestaurantModel(
        name=restaurant.name,
        address=restaurant.address,
        contact_number=restaurant.contact_number,
        contact_email=restaurant.contact_email,
        instagram_link=restaurant.instagram_link,
        website_link=restaurant.website_link,
        wifi_ssid=restaurant.wifi_ssid,
        wifi_password=restaurant.wifi_password,
        working_hours=restaurant.working_hours.model_dump(mode="json")
    )
    
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

@router.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant