from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

class Plant(Base):

    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    water_amount = Column(Numeric)
    unit = Column(String)
    frequency_days = Column(Integer)
    last_watered = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

    @hybrid_property
    def needs_watering(self):
        if not self.last_watered:
            return True  # if never watered, it needs watering

        days_since_watered = (date.today() - self.last_watered).days
        return days_since_watered >= self.frequency_days

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
