
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.insurance_product import InsuranceProductRepository
from app.schemas.insurance_product import (
    InsuranceProductCreate,
    InsuranceProductUpdate,
    InsuranceProductResponse
)


router = APIRouter(
    prefix="/insurance-products",
    tags=["Insurance Products"]
)


# Create an insurance product
@router.post(
    "/",
    response_model=InsuranceProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_insurance_product(
    product_data: InsuranceProductCreate,
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)

    existing_product = product_repo.get_by_name(product_data.name)

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insurance product already exists"
        )

    return product_repo.create(product_data)


# Get all insurance products
@router.get(
    "/",
    response_model=list[InsuranceProductResponse]
)
def get_insurance_products(
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)

    return product_repo.get_all()


# Get insurance product by ID
@router.get(
    "/{product_id}",
    response_model=InsuranceProductResponse
)
def get_insurance_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance product not found"
        )

    return product


# Update insurance product
@router.patch(
    "/{product_id}",
    response_model=InsuranceProductResponse
)
def update_insurance_product(
    product_id: int,
    product_data: InsuranceProductUpdate,
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    new_name = update_data.get("name")

    if new_name and new_name != product.name:
        existing_product = product_repo.get_by_name(new_name)

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another insurance product already uses this name"
            )

    return product_repo.update(product, product_data)


# Deactivate insurance product
@router.patch(
    "/{product_id}/deactivate",
    response_model=InsuranceProductResponse
)
def deactivate_insurance_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance product not found"
        )

    return product_repo.deactivate(product)
