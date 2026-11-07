from app.repositories.customer_repo import CustomerRepository
from app.repositories.insurance_claim import InsuranceClaimRepository
from app.repositories.insurance_package import InsurancePackageRepository
from app.repositories.insurance_policy import InsurancePolicyRepository
from app.repositories.insurance_product import InsuranceProductRepository
from app.repositories.payment_repo import PaymentRepository
from app.repositories.user_repo import UserRepository

__all__ = [
    "CustomerRepository",
    "InsuranceClaimRepository",
    "InsurancePackageRepository",
    "InsurancePolicyRepository",
    "InsuranceProductRepository",
    "PaymentRepository",
    "UserRepository",
]
