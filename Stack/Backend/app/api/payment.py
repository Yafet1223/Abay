from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.payment_repo import PaymentRepository
from app.repositories.insurance_policy import InsurancePolicyRepository
from app.schemas.insurance_payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# CREATE PAYMENT
@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    payment_repo = PaymentRepository(db)
    policy_repo = InsurancePolicyRepository(db)

    # Check whether the policy exists
    policy = policy_repo.get_by_id(payment_data.policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    # Create payment
    return payment_repo.create(payment_data)


# GET ALL PAYMENTS
@router.get("/", response_model=list[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    payment_repo = PaymentRepository(db)

    return payment_repo.get_all()


# GET PAYMENTS BY POLICY
@router.get("/policy/{policy_id}", response_model=list[PaymentResponse])
def get_payments_by_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)
    payment_repo = PaymentRepository(db)

    policy = policy_repo.get_by_id(policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    return payment_repo.get_by_policy_id(policy_id)


# GET ONE PAYMENT
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment_repo = PaymentRepository(db)

    payment = payment_repo.get_by_id(payment_id)

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment


# UPDATE PAYMENT
@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment_repo = PaymentRepository(db)

    payment = payment_repo.get_by_id(payment_id)

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment_repo.update(payment, payment_data)
