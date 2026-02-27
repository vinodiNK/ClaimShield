# main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models

app = FastAPI(title="ClaimShield API")

# Create tables automatically
Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "ClaimShield Backend Running with PostgreSQL"}


@app.post("/submit-claim")
def submit_claim(
    name: str,
    amount: float,
    description: str,
    db: Session = Depends(get_db)
):

    new_claim = models.Claim(
        claimant_name=name,
        claim_amount=amount,
        description=description
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return {
        "message": "Claim submitted successfully",
        "claim_id": new_claim.id
    }


@app.get("/claims")
def get_all_claims(db: Session = Depends(get_db)):
    claims = db.query(models.Claim).all()
    return claims