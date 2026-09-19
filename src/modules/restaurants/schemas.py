from pydantic import BaseModel, ConfigDict, Field
from datetime import time

class DayHours(BaseModel):
    start: time | None = None
    end: time | None = None
    is_closed: bool = Field(default=False)

class WorkingHours(BaseModel):
    model_config = ConfigDict(extra="forbid")
    monday: DayHours = Field(default_factory=DayHours)
    tuesday: DayHours = Field(default_factory=DayHours)
    wednesday: DayHours = Field(default_factory=DayHours)
    thursday: DayHours = Field(default_factory=DayHours)
    friday: DayHours = Field(default_factory=DayHours)
    saturday: DayHours = Field(default_factory=DayHours)
    sunday: DayHours = Field(default_factory=DayHours)


class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    name: str = Field(...)
    description: str | None = Field(None)
    longitude: str | None = Field(None)
    latitude: str | None = Field(None)
    wifi_name: str | None = Field(None)
    wifi_password: str | None = Field(None)
    phone_number: str | None = Field(None)
    email: str = Field(...)
    working_hours: WorkingHours = Field(default_factory=WorkingHours)

class RestaurantCreate(BaseModel):
    name: str = Field(...)
    description: str | None = Field(None)
    longitude: str | None = Field(None)
    latitude: str | None = Field(None)
    wifi_name: str | None = Field(None)
    wifi_password: str | None = Field(None)
    phone_number: str | None = Field(None)
    email: str = Field(...)

