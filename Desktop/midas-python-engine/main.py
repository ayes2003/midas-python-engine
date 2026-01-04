from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Midas Financial Engine")

@app.get("/balance/{user_id}")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "balance": user.balance}

# Run this with: uvicorn main:app --reload