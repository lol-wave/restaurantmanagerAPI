from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = {
        "from_attributes": True,
    }

    id: int
    username: str
    email: EmailStr
    phone_number: str
    full_name: str