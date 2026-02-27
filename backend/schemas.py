# schemas.py

from pydantic import BaseModel

class ClaimCreate(BaseModel):
    name: str
    amount: float
    description: str


class ClaimResponse(BaseModel):
    id: int
    claimant_name: str
    claim_amount: float
    description: str
    fraud_score: float
    status: str

    class Config:
        from_attributes = True