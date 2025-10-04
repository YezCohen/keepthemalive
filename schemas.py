from pydantic import BaseModel
from datetime import date

class PlantBase(BaseModel):

    id: int
    name : str
    location: str
    water_amount: float
    unit: str
    frequency_days: int
    last_watered: date | None = None
    needs_watering: bool | None = None

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int

    class Config:
        from_attributes = True