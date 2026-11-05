from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create a payment
    def create(self, payment_data: PaymentCreate) -> Payment:
        payment = Payment(**payment_data.model_dump())

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment

    # Get payment by ID
    def get_by_id(self, payment_id: int) -> Payment | None:
        statement = select(Payment).where(
            Payment.id == payment_id
        )
        return self.db.scalar(statement)

    # Get all payments
    def get_all(self) -> list[Payment]:
        statement = select(Payment)
        return list(self.db.scalars(statement).all())

    # Get payments belonging to a policy
    def get_by_policy_id(self, policy_id: int) -> list[Payment]:
        statement = select(Payment).where(
            Payment.policy_id == policy_id
        )
        return list(self.db.scalars(statement).all())

    # Update payment
    def update(
        self,
        payment: Payment,
        payment_data: PaymentUpdate
    ) -> Payment:

        update_data = payment_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(payment, field, value)

        self.db.commit()
        self.db.refresh(payment)

        return payment

    # Get payment by transaction reference
    def get_by_transaction_reference(
        self,
        transaction_reference: str
    ) -> Payment | None:

        statement = select(Payment).where(
            Payment.transaction_reference == transaction_reference
        )
        return self.db.scalar(statement)