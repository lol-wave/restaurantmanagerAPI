from pydantic import BaseModel, ConfigDict, Field

class MenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    restaurant_id: int
    categories: list["CategoryResponse"] = Field(default_factory=list)

class MenuCreate(BaseModel):
    name: str
    restaurant_id: int

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    menu_id: int
    name: str
    items: list["ItemResponse"] = Field(default_factory=list)

class CategoryCreate(BaseModel):
    menu_id: int
    name: str

class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    picture_url: str | None = None
    category_id: int
    options: list["ItemOptionResponse"] = Field(default_factory=list)

class ItemOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    option_name: str
    price: int
    item_id: int
