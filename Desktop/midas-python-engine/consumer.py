import json
import requests
from confluent_kafka import Consumer, KafkaException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Transaction

# Configuration
KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'midas_python_group',
    'auto.offset.reset': 'earliest'
}
# This points to the external bonus service (mocked or real)
INCENTIVE_API_URL = "http://localhost:8080/incentive"

def process_transaction(msg_value):
    """
    Core Logic: 
    1. Parse JSON
    2. Check for Fraud (High Value)
    3. Validate User
    4. Call External API for Bonus
    5. Update Database
    """
    db: Session = SessionLocal()
    try:
        data = json.loads(msg_value)
        sender_name = data.get("sender")
        amount = float(data.get("amount"))

        # --- NOVELTY FEATURE: FRAUD GUARD ---
        # Rule: Automatically block transactions over $2000
        if amount > 2000:
            print(f"🚨 FRAUD ALERT: Transaction of ${amount} from {sender_name} was BLOCKED.")
            # We log it, but we DO NOT update the balance.
            return 
        # ------------------------------------

        # 1. Find Sender in Database
        user = db.query(User).filter(User.username == sender_name).first()
        if not user:
            print(f"User {sender_name} not found. Skipping.")
            return

        # 2. Call External Incentive API (Microservice Integration)
        # We wrap this in try/except so the main transaction doesn't fail if the API is down
        bonus = 0
        try:
            response = requests.post(INCENTIVE_API_URL, json=data, timeout=2)
            if response.status_code == 200:
                bonus = response.json().get("amount", 0)
        except Exception as e:
            # In a real app, we might log this to a monitoring tool
            print(f"⚠️ Incentive API unavailable (skipping bonus): {e}")

        # 3. Update Balance
        user.balance = user.balance - amount + bonus
        
        # 4. Save Transaction Record
        tx = Transaction(sender=sender_name, amount=amount, recipient=data.get("recipient"))
        db.add(tx)
        db.commit()
        
        print(f"✅ Processed: {sender_name} sent ${amount}. Bonus: ${bonus}. New Balance: ${user.balance}")

    except Exception as e:
        print(f"❌ Error processing message: {e}")
    finally:
        db.close()

def start_consumer():
    """
    Main loop that listens to the Kafka topic.
    (This requires a running Kafka server to work)
    """
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe(['midas-transactions'])

    try:
        print("Listening for Kafka messages...")
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            # Send the raw message to our logic function
            process_transaction(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    start_consumer()