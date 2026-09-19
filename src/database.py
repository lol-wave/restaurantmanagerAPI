from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



engine = create_engine("sqlite:///./main.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from .modules.users.models import UserModel
from .modules.restaurants.models import RestaurantModel, ContactModel
from .modules.menus.models import MenuModel, CategoryModel, ItemModel, ItemOptionModel

Base.metadata.create_all(engine)