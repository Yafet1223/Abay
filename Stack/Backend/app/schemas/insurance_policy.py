from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.insurance_policy import PolicyStatus


# Shared policy fields
class InsurancePolicyBase(BaseModel):
    customer_id: int
    package_id: int
    start_date: date
    end_date: date
    premium_amount: Decimal = Field(gt=0)
    coverage_amount: Decimal = Field(gt=0)


# Creating a policy
class InsurancePolicyCreate(InsurancePolicyBase):
    pass


# Updating a policy
class InsurancePolicyUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    premium_amount: Decimal | None = Field(default=None, gt=0)
    coverage_amount: Decimal | None = Field(default=None, gt=0)
    status: PolicyStatus | None = None


# Returning policy information
class InsurancePolicyResponse(InsurancePolicyBase):
    id: int
    policy_number: str
    status: PolicyStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)