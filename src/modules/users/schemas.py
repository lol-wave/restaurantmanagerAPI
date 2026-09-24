from pydantic import BaseModel, ConfigDict, EmailStr

from ...modules.restaurants.schemas import RestaurantResponse

class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    username: str
    email: EmailStr
    phone_number: str
    full_name: str
    restaurants: list[RestaurantResponse] = []

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    full_name: str
    password: str
    password_confirm: str

class UserLogin(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    user: UserResponse
    tokens: dict[str, str]


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str