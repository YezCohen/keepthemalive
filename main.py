from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, date
from sqlalchemy.orm import Session
import models, schemas, security
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keep Them Alive", version="1.0.0")

origins = [
    "http://localhost:5173",  # frontend URL
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

# Look for the token in the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Find and return the current user based on the JWT token provided in the request.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# Create a new plant
@app.post("/plants/", response_model=schemas.Plant)
def create_plant(
    plant: schemas.PlantCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    db_plant = models.Plant(**plant.dict(), owner_id=current_user.id)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

# Read all plants
@app.get("/plants/", response_model=list[schemas.Plant])
def read_plants(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
    ):

    return db.query(models.Plant).filter(models.Plant.owner_id == current_user.id).all()

# Update Watering
@app.post("/plants/{plant_id}/water/", response_model=schemas.Plant)
def water_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.last_watered = date.today()
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

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # --- הוסף את ארבע השורות הבאות כאן ---
    print("--- DEBUGGING PASSWORD ---")
    print(f"Password Type: {type(user.password)}")
    print(f"Password Value: '{user.password}'")
    print(f"Password Length: {len(user.password)}")
    print(f"Password Representation (repr): {repr(user.password)}")
    print("--------------------------")
    # ------------------------------------

    # Create user with hashed password
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db)
):
    # Find user in the database
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    # Make sure the user exists and the password is correct
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the access token
    access_token = security.create_access_token(
        data={"sub": user.email}
    )

    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}