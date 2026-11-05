
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class InsurancePackage(Base):
    __tablename__ = "insurance_packages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("insurance_products.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    base_premium: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    coverage_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    product = relationship(
        "InsuranceProduct",
        back_populates="packages"
    )
