
import enum

from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CustomerType(str, enum.Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    customer_type: Mapped[CustomerType] = mapped_column(
        Enum(CustomerType, name="customer_type"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
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
