from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.payment import PaymentStatus, PaymentMethod


# Shared payment fields
class PaymentBase(BaseModel):
    policy_id: int
    amount: Decimal = Field(gt=0)
    payment_method: PaymentMethod
    transaction_reference: str | None = None


# Creating a payment
class PaymentCreate(PaymentBase):
    pass


# Updating a payment
class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = None
    transaction_reference: str | None = None


# Returning payment information
class PaymentResponse(PaymentBase):
    id: int
    status: PaymentStatus
    paid_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)