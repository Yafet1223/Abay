from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.session import engine
from app.api.customer import router as customer_router
from app.api.user import router as user_router
from app.api.insurance_product import router as insurance_product_router
from app.api.insurance_package import router as insurance_package_router
from app.api.insurance_policy import router as insurance_policy_router
from app.api.insurance_claim import router as insurance_claim_router
from app.api.payment import router as payment_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# Register all API routers
app.include_router(customer_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(insurance_product_router, prefix="/api")
app.include_router(insurance_package_router, prefix="/api")
app.include_router(insurance_policy_router, prefix="/api")
app.include_router(insurance_claim_router, prefix="/api")
app.include_router(payment_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Insurance CRM API"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "connected"}

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
