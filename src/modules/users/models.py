from ...database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True, 
        index=True
    )

    username = Column(
        String(30), 
        unique=True
    )
    
    email = Column(
        String(255), 
        unique=True, 
        index=True
    )
    
    phone_number = Column(
        String,
        unique=True, 
        index=True
    )
    
    full_name = Column(
        String(75), 
        nullable=True
    )

    hashed_password = Column(
        String, 
        nullable=False
    )

    restaurants = relationship(
        "RestaurantModel", 
        back_populates="owner"
    )