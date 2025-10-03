from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keep Them Alive", version="1.0.0")

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
    return db.query(models.Plant).all()

# Update Watering
@app.post("/plants/{plant_id}/water", response_model=schemas.Plant)
def water_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    from datetime import date
    plant.last_watered = date.today()
    db.commit()
    db.refresh(plant)
    return plant

# Delete a plant
@app.delete("/plants/{plant_id}", response_model=dict)
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}