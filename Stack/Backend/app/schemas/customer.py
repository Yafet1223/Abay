
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.customer import CustomerType


# Shared customer fields
class CustomerBase(BaseModel):
    customer_type: CustomerType
    name: str
    email: EmailStr | None = None
    phone: str
    address: str | None = None


# Used when creating a customer
class CustomerCreate(CustomerBase):
    pass


# Used when updating a customer
class CustomerUpdate(BaseModel):
    customer_type: CustomerType | None = None
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool | None = None


# Used when returning customer information
class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)