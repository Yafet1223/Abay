from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_policy import InsurancePolicy
from app.schemas.insurance_policy import (
    InsurancePolicyCreate,
    InsurancePolicyUpdate
)


class InsurancePolicyRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create an insurance policy
    def create(self, policy_data: InsurancePolicyCreate, policy_number: str) -> InsurancePolicy:
        policy = InsurancePolicy(
            **policy_data.model_dump(),
            policy_number=policy_number
        )

        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)

        return policy

    # Get policy by ID
    def get_by_id(self, policy_id: int) -> InsurancePolicy | None:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.id == policy_id
        )
        return self.db.scalar(statement)

    # Get policy by policy number
    def get_by_policy_number(self, policy_number: str) -> InsurancePolicy | None:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.policy_number == policy_number
        )
        return self.db.scalar(statement)

    # Get all policies
    def get_all(self) -> list[InsurancePolicy]:
        statement = select(InsurancePolicy)
        return list(self.db.scalars(statement).all())

    # Get policies by customer ID
    def get_by_customer_id(self, customer_id: int) -> list[InsurancePolicy]:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.customer_id == customer_id
        )
        return list(self.db.scalars(statement).all())

    # Update policy
    def update(
        self,
        policy: InsurancePolicy,
        policy_data: InsurancePolicyUpdate
    ) -> InsurancePolicy:
        update_data = policy_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(policy, field, value)

        self.db.commit()
        self.db.refresh(policy)

        return policy
