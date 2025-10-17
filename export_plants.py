import json
from database import SessionLocal
from models import Plant

def export_data():
    db = SessionLocal()
    try:
        print("🌱 מתחבר למסד הנתונים ומייצא את העציצים...")
        plants = db.query(Plant).all()
        
        plants_data = []
        for plant in plants:
            plants_data.append({
                "name": plant.name,
                "location": plant.location,
                "water_amount": str(plant.water_amount), # Convert Decimal to string for JSON serialization
                "unit": plant.unit,
                "frequency_days": plant.frequency_days,
                "last_watered": plant.last_watered.isoformat() if plant.last_watered else None,
            })
        
        with open("plants_backup.json", "w", encoding="utf-8") as f:
            json.dump(plants_data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ הסתיים בהצלחה! יוצאו {len(plants_data)} עציצים לקובץ plants_backup.json")

    finally:
        db.close()

if __name__ == "__main__":
    export_data()