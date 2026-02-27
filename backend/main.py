# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models
import schemas
import fraud_engine

app = FastAPI(title="ClaimShield API")

# Create database tables automatically
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "ClaimShield Backend Running with PostgreSQL"}


# ✅ Submit Claim (Now Uses Pydantic + Fraud Engine)
@app.post("/submit-claim", response_model=schemas.ClaimResponse)
def submit_claim(claim: schemas.ClaimCreate, db: Session = Depends(get_db)):

    # Calculate fraud score
    fraud_score = fraud_engine.calculate_fraud_score(
        claim.amount,
        claim.description
    )

    # Determine claim status
    status = fraud_engine.determine_status(fraud_score)

    # Create claim object
    new_claim = models.Claim(
        claimant_name=claim.name,
        claim_amount=claim.amount,
        description=claim.description,
        fraud_score=fraud_score,
        status=status
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return new_claim


# ✅ Get All Claims
@app.get("/claims", response_model=list[schemas.ClaimResponse])
def get_all_claims(db: Session = Depends(get_db)):
    return db.query(models.Claim).all()


# ✅ Get Single Claim
@app.get("/claims/{claim_id}", response_model=schemas.ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):

    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim