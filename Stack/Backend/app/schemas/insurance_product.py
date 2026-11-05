from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InsuranceProductBase(BaseModel):
    name: str
    description: str | None = None


class InsuranceProductCreate(InsuranceProductBase):
    pass


class InsuranceProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class InsuranceProductResponse(InsuranceProductBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)