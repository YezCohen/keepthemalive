import json
from decimal import Decimal
from datetime import date
from database import SessionLocal
from models import Plant

# ---  User that we want to import the plants to ---
NEW_USER_ID = 1
# -----------------------------------------

def import_data():
    db = SessionLocal()
    try:
        print(f"📥 קורא את העציצים מהקובץ ומייבא אותם עבור משתמש עם ID={NEW_USER_ID}...")
        
        with open("plants_backup.json", "r", encoding="utf-8") as f:
            plants_data = json.load(f)
            
        for plant_dict in plants_data:
            new_plant = Plant(
                name=plant_dict["name"],
                location=plant_dict["location"],
                water_amount=Decimal(plant_dict["water_amount"]),
                unit=plant_dict["unit"],
                frequency_days=plant_dict["frequency_days"],
                last_watered=date.fromisoformat(plant_dict["last_watered"]) if plant_dict["last_watered"] else None,
                owner_id=NEW_USER_ID # Assign to the new user ID
            )
            db.add(new_plant)
            
        db.commit()
        print(f"✅ הסתיים בהצלחה! יובאו {len(plants_data)} עציצים.")
        
    finally:
        db.close()

if __name__ == "__main__":
    import_data()