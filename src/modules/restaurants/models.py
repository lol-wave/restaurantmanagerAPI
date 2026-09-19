from ...database import Base
from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

class RestaurantModel(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    wifi_name = Column(String, nullable=True)
    wifi_password = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=False)
    contacts = relationship("ContactModel", back_populates="restaurant")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("UserModel", back_populates="restaurants")
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=True)
    working_hours = Column(JSON, nullable=True)


class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    instagram = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    telegram = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant = relationship("RestaurantModel", back_populates="contacts")
