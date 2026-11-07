from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.customer_repo import CustomerRepository
from app.repositories.insurance_package import InsurancePackageRepository
from app.repositories.insurance_policy import InsurancePolicyRepository
from app.schemas.insurance_policy import (
    InsurancePolicyCreate,
    InsurancePolicyUpdate,
    InsurancePolicyResponse
)


router = APIRouter(
    prefix="/insurance-policies",
    tags=["Insurance Policies"]
)


# CREATE INSURANCE POLICY
@router.post(
    "/",
    response_model=InsurancePolicyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_insurance_policy(
    policy_data: InsurancePolicyCreate,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)
    customer_repo = CustomerRepository(db)
    package_repo = InsurancePackageRepository(db)

    # Validate customer exists
    customer = customer_repo.get_by_id(policy_data.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Validate insurance package exists and is active
    package = package_repo.get_by_id(policy_data.package_id)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance package not found"
        )
    if not package.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot issue policy for an inactive package"
        )

    # Validate dates
    if policy_data.start_date >= policy_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Policy end date must be after start date"
        )

    # Generate unique policy number
    policy_number = f"POL-{date.today().year}-{uuid4().hex[:8].upper()}"

    return policy_repo.create(policy_data, policy_number)


# GET ALL POLICIES
@router.get("/", response_model=list[InsurancePolicyResponse])
def get_insurance_policies(db: Session = Depends(get_db)):
    policy_repo = InsurancePolicyRepository(db)

    return policy_repo.get_all()


# GET ONE POLICY BY ID
@router.get("/{policy_id}", response_model=InsurancePolicyResponse)
def get_insurance_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)

    policy = policy_repo.get_by_id(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    return policy


# GET POLICIES BY CUSTOMER ID
@router.get("/customer/{customer_id}", response_model=list[InsurancePolicyResponse])
def get_policies_by_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)
    customer_repo = CustomerRepository(db)

    customer = customer_repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return policy_repo.get_by_customer_id(customer_id)


# UPDATE INSURANCE POLICY
@router.patch("/{policy_id}", response_model=InsurancePolicyResponse)
def update_insurance_policy(
    policy_id: int,
    policy_data: InsurancePolicyUpdate,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)

    policy = policy_repo.get_by_id(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    return policy_repo.update(policy, policy_data)

