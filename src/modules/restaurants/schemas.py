from pydantic import BaseModel, ConfigDict, Field
from datetime import time

class DayHours(BaseModel):
    start: time | None = None
    end: time | None = None
    is_closed: bool = Field(default=False, description="Indicates if the restaurant is closed on this day")

class WorkingHours(BaseModel):
    model_config = ConfigDict(extra="forbid")
    monday: DayHours = Field(default_factory=DayHours, description="Working hours for Monday")
    tuesday: DayHours = Field(default_factory=DayHours, description="Working hours for Tuesday")
    wednesday: DayHours = Field(default_factory=DayHours, description="Working hours for Wednesday")
    thursday: DayHours = Field(default_factory=DayHours, description="Working hours for Thursday")
    friday: DayHours = Field(default_factory=DayHours, description="Working hours for Friday")
    saturday: DayHours = Field(default_factory=DayHours, description="Working hours for Saturday")
    sunday: DayHours = Field(default_factory=DayHours, description="Working hours for Sunday")





class RestaurantBase(BaseModel):
    name: str = Field(..., description="The name of the restaurant")
    address: str = Field(..., description="The address of the restaurant")
    contact_number: str = Field(..., description="The contact number of the restaurant")
    contact_email: str = Field(..., description="The contact email of the restaurant")
    instagram_link: str | None = Field(None, description="The Instagram link of the restaurant")
    website_link: str | None = Field(None, description="The website link of the restaurant")
    wifi_ssid: str | None = Field(None, description="The Wi-Fi Name (SSID) of the restaurant")
    wifi_password: str | None = Field(None, description="The Wi-Fi password of the restaurant")
    working_hours: WorkingHours = Field(default_factory=WorkingHours, description="The working hours of the restaurant")

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="The unique identifier of the restaurant")
    name: str = Field(..., description="The name of the restaurant")
    owner_id: int | None = Field(None, description="The unique identifier of the owner of the restaurant")