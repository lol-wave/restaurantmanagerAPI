from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    model_config=ConfigDict("from_attributes" = True)
    id: int
    username: str
    email: EmailStr
    phone_number: str
    full_name: str
    
class UserRegister(BaseModel):
	username: str
	email: EmailStr
	phone_number: str
	full_name: str
	password1: str
	password2: str

class UserLogin(BaseModel):
	login: str
	password: str