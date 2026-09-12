from ...database import Base
from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

class RestaurantModel(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    instagram_link = Column(String, nullable=True)
    website_link = Column(String, nullable=True)
    wifi_ssid = Column(String, nullable=True)
    wifi_password = Column(String, nullable=True)
    working_hours = Column(JSON, nullable=False, default=dict)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("UserModel", back_populates="restaurants")