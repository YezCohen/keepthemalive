from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean
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

    @hybrid_property
    def needs_watering(self):
        if not self.last_watered:
            return True  # אם מעולם לא הושקה, צריך להשקות

        days_since_watered = (date.today() - self.last_watered).days
        return days_since_watered >= self.frequency_days