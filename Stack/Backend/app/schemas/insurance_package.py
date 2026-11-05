from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


# Shared package fields
class InsurancePackageBase(BaseModel):
    product_id: int
    name: str
    description: str | None = None
    base_premium: Decimal
    coverage_limit: Decimal | None = None


# Creating a package
class InsurancePackageCreate(InsurancePackageBase):
    pass


# Updating a package
class InsurancePackageUpdate(BaseModel):
    product_id: int | None = None
    name: str | None = None
    description: str | None = None
    base_premium: Decimal | None = None
    coverage_limit: Decimal | None = None
    is_active: bool | None = None


# Returning package information
class InsurancePackageResponse(InsurancePackageBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)