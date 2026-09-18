from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from .models import RestaurantModel
from .schemas import RestaurantBase, RestaurantCreate, RestaurantResponse

router = APIRouter()

