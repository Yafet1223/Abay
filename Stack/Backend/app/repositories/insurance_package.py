from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_package import InsurancePackage
from app.schemas.insurance_package import (
    InsurancePackageCreate,
    InsurancePackageUpdate
)


class InsurancePackageRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create an insurance package
    def create(self, package_data: InsurancePackageCreate) -> InsurancePackage:
        package = InsurancePackage(**package_data.model_dump())

        self.db.add(package)
        self.db.commit()
        self.db.refresh(package)

        return package

    # Get package by ID
    def get_by_id(self, package_id: int) -> InsurancePackage | None:
        statement = select(InsurancePackage).where(
            InsurancePackage.id == package_id
        )
        return self.db.scalar(statement)

    # Get all packages
    def get_all(self) -> list[InsurancePackage]:
        statement = select(InsurancePackage)
        return list(self.db.scalars(statement).all())

    # Get packages by product ID
    def get_by_product_id(self, product_id: int) -> list[InsurancePackage]:
        statement = select(InsurancePackage).where(
            InsurancePackage.product_id == product_id
        )
        return list(self.db.scalars(statement).all())

    # Update package
    def update(
        self,
        package: InsurancePackage,
        package_data: InsurancePackageUpdate
    ) -> InsurancePackage:

        update_data = package_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(package, field, value)

        self.db.commit()
        self.db.refresh(package)

        return package

    # Deactivate package
    def deactivate(self, package: InsurancePackage) -> InsurancePackage:
        package.is_active = False

        self.db.commit()
        self.db.refresh(package)

        return package