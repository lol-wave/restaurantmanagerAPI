from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import MenuModel, CategoryModel, ItemModel, ItemOptionModel
from .schemas import CategoryCreate, MenuCreate, MenuResponse, CategoryResponse, ItemResponse, ItemOptionResponse
from ...dependencies import get_db, get_current_user_id
from ..restaurants.models import RestaurantModel

menu_router = APIRouter()

@menu_router.post("/menus/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == menu.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    is_owner = restaurant.owner_id == current_user_id
    if not is_owner:
        raise HTTPException(status_code=403, detail="You are not the owner of this restaurant")

    db_menu = MenuModel(name=menu.name, restaurant_id=menu.restaurant_id)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@menu_router.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    menu = db.query(MenuModel).filter(MenuModel.id == category.menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == menu.restaurant_id).first()
    is_owner = restaurant.owner_id == current_user_id
    if not is_owner:
        raise HTTPException(status_code=403, detail="You are not the owner of this restaurant")

    db_category = CategoryModel(name=category.name, menu_id=category.menu_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category