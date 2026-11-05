from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_product import InsuranceProduct
from app.schemas.insurance_product import (
    InsuranceProductCreate,
    InsuranceProductUpdate
)


class InsuranceProductRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create an insurance product
    def create(self, product_data: InsuranceProductCreate) -> InsuranceProduct:
        product = InsuranceProduct(**product_data.model_dump())

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    # Get product by ID
    def get_by_id(self, product_id: int) -> InsuranceProduct | None:
        statement = select(InsuranceProduct).where(
            InsuranceProduct.id == product_id
        )
        return self.db.scalar(statement)

    # Get product by name
    def get_by_name(self, name: str) -> InsuranceProduct | None:
        statement = select(InsuranceProduct).where(
            InsuranceProduct.name == name
        )
        return self.db.scalar(statement)

    # Get all products
    def get_all(self) -> list[InsuranceProduct]:
        statement = select(InsuranceProduct)
        return list(self.db.scalars(statement).all())

    # Update product
    def update(
        self,
        product: InsuranceProduct,
        product_data: InsuranceProductUpdate
    ) -> InsuranceProduct:

        update_data = product_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)

        return product

    # Deactivate product
    def deactivate(self, product: InsuranceProduct) -> InsuranceProduct:
        product.is_active = False

        self.db.commit()
        self.db.refresh(product)

        return product