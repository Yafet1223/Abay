import enum

from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ClaimStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SETTLED = "settled"


class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    claim_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    policy_id: Mapped[int] = mapped_column(
        ForeignKey("insurance_policies.id"),
        nullable=False,
        index=True
    )

    incident_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    claimed_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    approved_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    status: Mapped[ClaimStatus] = mapped_column(
        Enum(ClaimStatus, name="claim_status"),
        default=ClaimStatus.SUBMITTED,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    policy = relationship("InsurancePolicy")