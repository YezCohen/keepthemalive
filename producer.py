import os
import json
import time
from kafka import KafkaProducer
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Load configuration from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
PLANTS_TOPIC = os.getenv("PLANTS_TOPIC", "watering_schedule")

def create_producer():
    """
    Trying to create a Kafka producer with retries until successful.
    It's important to ensure Kafka is up before proceeding.
    """
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Producer התחבר בהצלחה ל-Kafka")
            return producer
        except Exception as e:
            print(f"⏳ ממתין ל-Kafka... נכשל בהתחברות עם שגיאה: {e}")
            time.sleep(5)

def check_plants_and_notify(db: Session, producer: KafkaProducer):
    """
    Checks which plants need watering and sends notifications via Kafka.
    """
    print("⏰ בודק אילו עציצים צריכים השקיה...")
    
    # Same logic as before to find plants that need watering
    plants_to_water = db.query(models.Plant).all()
    
    notifications_sent = 0

    for plant in plants_to_water:
        # Using the existing method to check if watering is needed
        if plant.needs_watering:
            message = {
                "plant_id": plant.id,
                "plant_name": plant.name,
                "owner_id": plant.owner_id,
                "message": f"הגיע הזמן להשקות את {plant.name}!"
            }
            
            producer.send(PLANTS_TOPIC, message)
            print(f"📨 נשלחה הודעה עבור עציץ: {plant.name} (ID: {plant.id})")
            notifications_sent += 1

    if notifications_sent > 0:
        producer.flush() # Make sure all messages are sent
        print(f"📬 סה\"כ נשלחו {notifications_sent} התראות.")
    else:
        print("💧 כל העציצים מושקים, אין צורך בהתראות.")


if __name__ == "__main__":
    db = SessionLocal()
    producer = create_producer()
    try:
        # In endless loop, check every 24 hours
        while True:
            check_plants_and_notify(db, producer)
            print("😴 הולך לישון ל-24 שעות...")
            time.sleep(60) # * 60 * 24) # Sleep for 24 hours
    except KeyboardInterrupt:
        print(" shutting down producer...")
    finally:
        producer.close()
        db.close()