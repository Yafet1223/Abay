from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create a customer
    def create(self, customer_data: CustomerCreate) -> Customer:

        customer = Customer(
            **customer_data.model_dump()
        )

        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    # Get customer by ID
    def get_by_id(self, customer_id: int) -> Customer | None:

        statement = select(Customer).where(
            Customer.id == customer_id
        )

        return self.db.scalar(statement)

    # Get customer by email
    def get_by_email(self, email: str) -> Customer | None:

        statement = select(Customer).where(
            Customer.email == email
        )

        return self.db.scalar(statement)

    # Get all customers
    def get_all(self) -> list[Customer]:

        statement = select(Customer)

        return list(self.db.scalars(statement).all())

    # Update customer
    def update(
        self,
        customer: Customer,
        customer_data: CustomerUpdate
    ) -> Customer:

        update_data = customer_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(customer, field, value)

        self.db.commit()
        self.db.refresh(customer)

        return customer

    # Deactivate customer
    def deactivate(self, customer: Customer) -> Customer:

        customer.is_active = False

        self.db.commit()
        self.db.refresh(customer)

        return customer