from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.insurance_claim import InsuranceClaimRepository
from app.repositories.insurance_policy import InsurancePolicyRepository
from app.schemas.insurance_claim import (
    InsuranceClaimCreate,
    InsuranceClaimUpdate,
    InsuranceClaimResponse
)


router = APIRouter(
    prefix="/insurance-claims",
    tags=["Insurance Claims"]
)


# CREATE INSURANCE CLAIM
@router.post(
    "/",
    response_model=InsuranceClaimResponse,
    status_code=status.HTTP_201_CREATED
)
def create_claim(
    claim_data: InsuranceClaimCreate,
    db: Session = Depends(get_db)
):
    claim_repo = InsuranceClaimRepository(db)
    policy_repo = InsurancePolicyRepository(db)

    # Check whether the policy exists
    policy = policy_repo.get_by_id(claim_data.policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    # Check whether the policy is active
    if str(policy.status).lower() != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Claims can only be submitted for active policies"
        )

    # Check incident date
    if claim_data.incident_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incident date cannot be in the future"
        )

    # Generate unique claim number
    claim_number = f"CLM-{date.today().year}-{uuid4().hex[:8].upper()}"

    # Create claim
    return claim_repo.create(
        claim_data,
        claim_number
    )


# GET ALL CLAIMS
@router.get("/", response_model=list[InsuranceClaimResponse])
def get_claims(db: Session = Depends(get_db)):
    claim_repo = InsuranceClaimRepository(db)

    return claim_repo.get_all()


# GET CLAIMS BY POLICY
@router.get("/policy/{policy_id}", response_model=list[InsuranceClaimResponse])
def get_claims_by_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    policy_repo = InsurancePolicyRepository(db)
    claim_repo = InsuranceClaimRepository(db)

    policy = policy_repo.get_by_id(policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance policy not found"
        )

    return claim_repo.get_by_policy_id(policy_id)


# GET ONE CLAIM
@router.get("/{claim_id}", response_model=InsuranceClaimResponse)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):
    claim_repo = InsuranceClaimRepository(db)

    claim = claim_repo.get_by_id(claim_id)

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance claim not found"
        )

    return claim
    

# UPDATE CLAIM
@router.patch("/{claim_id}", response_model=InsuranceClaimResponse)
def update_claim(
    claim_id: int,
    claim_data: InsuranceClaimUpdate,
    db: Session = Depends(get_db)
):
    claim_repo = InsuranceClaimRepository(db)

    claim = claim_repo.get_by_id(claim_id)

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance claim not found"
        )

    return claim_repo.update(claim, claim_data)
