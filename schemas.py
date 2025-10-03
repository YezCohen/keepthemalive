from pydantic import BaseModel

class PlantBase(BaseModel):

    name : str
    location: str
    water_amount: float
    unit: str
    frequency_days: int

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int

    class Config:
        from_attributes = True