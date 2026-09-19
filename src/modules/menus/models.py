from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ...database import Base

class MenuModel(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    categories = relationship("CategoryModel")

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    name = Column(String, nullable=False)
    items = relationship("ItemModel", back_populates="category")

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("CategoryModel", back_populates="items")
    options = relationship("ItemOptionModel", back_populates="item")

class ItemOptionModel(Base):
    __tablename__ = "item_options"

    id = Column(Integer, primary_key=True, index=True)
    option_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    item = relationship("ItemModel", back_populates="options")