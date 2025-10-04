from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, date
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keep Them Alive", version="1.0.0")

origins = [
    "http://localhost:5173",  # your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new plant
@app.post("/plants/", response_model=schemas.Plant)
def create_plant(plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    db_plant = models.Plant(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

# Read all plants
@app.get("/plants/", response_model=list[schemas.Plant])
def read_plants(db: Session = Depends(get_db)):
    plants = db.query(models.Plant).all()
    today = datetime.now().date()
    result = []

    for plant in plants:
        last_watered_date = None
        if plant.last_watered:
            try:
                last_watered_date = datetime.strptime(plant.last_watered, "%Y-%m-%d").date()
            except:
                pass

        needs_watering = False
        if last_watered_date:
            days_since_watered = (today - last_watered_date).days
            needs_watering = days_since_watered >= plant.frequency_days
        else:
            needs_watering = True  # Never watered

        plant_dict = {
            "id": plant.id,
            "name": plant.name,
            "location": plant.location,
            "water_amount": plant.water_amount,
            "unit": plant.unit,
            "frequency_days": plant.frequency_days,
            "last_watered": plant.last_watered,
            "needs_watering": needs_watering
        }
        result.append(plant_dict)

    return result

# Update Watering
@app.post("/plants/{plant_id}/water/", response_model=schemas.Plant)
def water_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.last_watered = date.today()
    plant.needs_watering = False
    db.commit()
    db.refresh(plant)
    return plant

# Delete a plant
@app.delete("/plants/{plant_id}/", response_model=dict)
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}