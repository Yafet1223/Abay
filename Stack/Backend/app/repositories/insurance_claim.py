from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_claim import InsuranceClaim
from app.schemas.insurance_claim import (
    InsuranceClaimCreate,
    InsuranceClaimUpdate
)


class InsuranceClaimRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create an insurance claim
    def create(
        self,
        claim_data: InsuranceClaimCreate,
        claim_number: str | None = None
    ) -> InsuranceClaim:
        if not claim_number:
            from datetime import date
            from uuid import uuid4
            claim_number = f"CLM-{date.today().year}-{uuid4().hex[:8].upper()}"

        claim = InsuranceClaim(
            **claim_data.model_dump(),
            claim_number=claim_number
        )

        self.db.add(claim)
        self.db.commit()
        self.db.refresh(claim)

        return claim

    # Get claim by ID
    def get_by_id(self, claim_id: int) -> InsuranceClaim | None:
        statement = select(InsuranceClaim).where(
            InsuranceClaim.id == claim_id
        )
        return self.db.scalar(statement)

    # Get claim by claim number
    def get_by_claim_number(self, claim_number: str) -> InsuranceClaim | None:
        statement = select(InsuranceClaim).where(
            InsuranceClaim.claim_number == claim_number
        )
        return self.db.scalar(statement)

    # Get all claims
    def get_all(self) -> list[InsuranceClaim]:
        statement = select(InsuranceClaim)
        return list(self.db.scalars(statement).all())

    # Get claims belonging to a policy
    def get_by_policy_id(self, policy_id: int) -> list[InsuranceClaim]:
        statement = select(InsuranceClaim).where(
            InsuranceClaim.policy_id == policy_id
        )
        return list(self.db.scalars(statement).all())

    # Update claim
    def update(
        self,
        claim: InsuranceClaim,
        claim_data: InsuranceClaimUpdate
    ) -> InsuranceClaim:
        update_data = claim_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(claim, field, value)

        self.db.commit()
        self.db.refresh(claim)

        return claim
