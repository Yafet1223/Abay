from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.insurance_claim import ClaimStatus


# Shared claim fields
class InsuranceClaimBase(BaseModel):
    policy_id: int
    incident_date: date
    description: str
    claimed_amount: Decimal = Field(gt=0)


# Creating a claim
class InsuranceClaimCreate(InsuranceClaimBase):
    pass


# Updating a claim
class InsuranceClaimUpdate(BaseModel):
    status: ClaimStatus | None = None
    approved_amount: Decimal | None = Field(default=None, gt=0)


# Returning claim information
class InsuranceClaimResponse(InsuranceClaimBase):
    id: int
    claim_number: str
    approved_amount: Decimal | None = None
    status: ClaimStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)