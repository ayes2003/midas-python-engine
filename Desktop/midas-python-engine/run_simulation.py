import json
import time
from consumer import process_transaction
from database import SessionLocal, engine, Base
from models import User

# 1. Setup: Create the Database and a Test User
print("⚙️  Setting up simulation environment...")
Base.metadata.create_all(bind=engine) # Ensure tables exist
db = SessionLocal()

# Check if test user exists, if not, create one
test_user = db.query(User).filter(User.username == "john_doe").first()
if not test_user:
    print("👤 Creating test user 'john_doe' with $1000...")
    test_user = User(username="john_doe", balance=1000.0)
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
else:
    # Reset balance to 1000 for a clean test every time
    test_user.balance = 1000.0
    db.commit()
    print(f"👤 User 'john_doe' found. Reset balance to: ${test_user.balance}")

print("-" * 50)
print("🚀 STARTING TRANSACTION SIMULATION")
print("-" * 50)

# 2. Simulate Incoming Kafka Messages
# These are the messages Kafka WOULD send if it were running
fake_kafka_messages = [
    # Case 1: Normal Transaction (Should Pass)
    '{"sender": "john_doe", "recipient": "amazon", "amount": 50.0}',
    
    # Case 2: FRAUD ATTEMPT (Should be BLOCKED)
    '{"sender": "john_doe", "recipient": "hacker_account", "amount": 5000.0}',
    
    # Case 3: Normal Transaction (Should Pass)
    '{"sender": "john_doe", "recipient": "netflix", "amount": 15.0}'
]

for msg in fake_kafka_messages:
    print(f"\n[Kafka] Received message: {msg}")
    
    # Pass the fake message directly to your logic function
    process_transaction(msg) 
    
    # Check the database to see if the balance changed
    db.refresh(test_user)
    print(f"   💰 Current Balance for john_doe: ${test_user.balance}")
    time.sleep(1) # Wait a second so you can read the output

print("\n" + "-" * 50)
print("✅ SIMULATION COMPLETE")
db.close()