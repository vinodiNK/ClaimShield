# models.py

from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claimant_name = Column(String, nullable=False)
    claim_amount = Column(Float, nullable=False)
    description = Column(Text)
    fraud_score = Column(Float, default=0)
    status = Column(String, default="SUBMITTED")