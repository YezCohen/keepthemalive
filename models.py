from sqlalchemy import Column, Integer, String, Numeric, Date
from database import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    water_amount = Column(Numeric)
    unit = Column(String)
    frequency_days = Column(Integer)
    last_watered = Column(Date)