from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ...database import Base

class MenuModel(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant = relationship("RestaurantModel", back_populates="menus")
    categories = relationship("CategoryModel", back_populates="menu")

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    menu = relationship("MenuModel", back_populates="categories")
    items = relationship("ItemModel", back_populates="category")

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    picture_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("CategoryModel", back_populates="items")