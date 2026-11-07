from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.insurance_package import InsurancePackageRepository
from app.repositories.insurance_product import InsuranceProductRepository
from app.schemas.insurance_package import (
    InsurancePackageCreate,
    InsurancePackageUpdate,
    InsurancePackageResponse
)


router = APIRouter(
    prefix="/insurance-packages",
    tags=["Insurance Packages"]
)


# Create an insurance package
@router.post(
    "/",
    response_model=InsurancePackageResponse,
    status_code=status.HTTP_201_CREATED
)
def create_insurance_package(
    package_data: InsurancePackageCreate,
    db: Session = Depends(get_db)
):
    package_repo = InsurancePackageRepository(db)
    product_repo = InsuranceProductRepository(db)

    # Check whether the product exists
    product = product_repo.get_by_id(package_data.product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance product not found"
        )

    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create a package under an inactive product"
        )

    return package_repo.create(package_data)


# Get all insurance packages
@router.get(
    "/",
    response_model=list[InsurancePackageResponse]
)
def get_insurance_packages(
    db: Session = Depends(get_db)
):
    package_repo = InsurancePackageRepository(db)

    return package_repo.get_all()


# Get package by ID
@router.get(
    "/{package_id}",
    response_model=InsurancePackageResponse
)
def get_insurance_package(
    package_id: int,
    db: Session = Depends(get_db)
):
    package_repo = InsurancePackageRepository(db)

    package = package_repo.get_by_id(package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance package not found"
        )

    return package


# Get packages belonging to a product
@router.get(
    "/product/{product_id}",
    response_model=list[InsurancePackageResponse]
)
def get_packages_by_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_repo = InsuranceProductRepository(db)
    package_repo = InsurancePackageRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance product not found"
        )

    return package_repo.get_by_product_id(product_id)


# Update insurance package
@router.patch(
    "/{package_id}",
    response_model=InsurancePackageResponse
)
def update_insurance_package(
    package_id: int,
    package_data: InsurancePackageUpdate,
    db: Session = Depends(get_db)
):
    package_repo = InsurancePackageRepository(db)

    package = package_repo.get_by_id(package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance package not found"
        )

    return package_repo.update(package, package_data)


# Deactivate insurance package
@router.patch(
    "/{package_id}/deactivate",
    response_model=InsurancePackageResponse
)
def deactivate_insurance_package(
    package_id: int,
    db: Session = Depends(get_db)
):
    package_repo = InsurancePackageRepository(db)

    package = package_repo.get_by_id(package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurance package not found"
        )

    return package_repo.deactivate(package)
