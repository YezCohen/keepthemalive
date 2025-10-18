import os
import json
import time
from kafka import KafkaConsumer

# Load settings from environment, just like in the producer
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
PLANTS_TOPIC = os.getenv("PLANTS_TOPIC", "watering_schedule")

def create_consumer():
    """
    Tries to connect to Kafka as a consumer. If it fails, waits and retries.
    """
    while True:
        try:
            consumer = KafkaConsumer(
                PLANTS_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                # group_id ensures that if we run multiple consumers, each message is read only once
                group_id='watering-notification-group' 
            )
            print("✅ Consumer התחבר בהצלחה ל-Kafka")
            return consumer
        except Exception as e:
            print(f"⏳ ממתין ל-Kafka... נכשל בהתחברות עם שגיאה: {e}")
            time.sleep(5)

def listen_for_messages():
    """
    Listens for messages from the topic in an infinite loop and prints them.
    """
    consumer = create_consumer()
    print(f"📬 מאזין להודעות חדשות ב-topic: {PLANTS_TOPIC}...")
    
    for message in consumer:
        # 'message.value' contains the JSON we sent from the producer
        watering_info = message.value
        print("\n-------------------------")
        print("📥 התקבלה הודעה חדשה:")
        print(f"   - מזהה עציץ: {watering_info.get('plant_id')}")
        print(f"   - שם עציץ: {watering_info.get('plant_name')}")
        print(f"   - תוכן ההודעה: {watering_info.get('message')}")
        print("-------------------------\n")
        # Here in the future, instead of printing, you will call the function that sends a WhatsApp notification
        # send_whatsapp_notification(watering_info)

if __name__ == "__main__":
    try:
        listen_for_messages()
    except KeyboardInterrupt:
        print(" shutting down consumer...")