
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.customer_repo import CustomerRepository
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# Create a customer
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    customer_repo = CustomerRepository(db)

    if customer_data.email:
        existing_customer = customer_repo.get_by_email(
            customer_data.email
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this email already exists"
            )

    return customer_repo.create(customer_data)


# Get all customers
@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):
    customer_repo = CustomerRepository(db)

    return customer_repo.get_all()


# Get customer by ID
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer_repo = CustomerRepository(db)

    customer = customer_repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# Update customer
@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer_repo = CustomerRepository(db)

    customer = customer_repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    update_data = customer_data.model_dump(exclude_unset=True)
    new_email = update_data.get("email")

    if new_email and new_email != customer.email:
        existing_customer = customer_repo.get_by_email(new_email)

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Email already belongs to another customer"
            )

    return customer_repo.update(customer, customer_data)


# Deactivate customer
@router.patch(
    "/{customer_id}/deactivate",
    response_model=CustomerResponse
)
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer_repo = CustomerRepository(db)

    customer = customer_repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer_repo.deactivate(customer)

