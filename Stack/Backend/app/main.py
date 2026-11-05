from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.session import engine
from app.api.customer import router as customer_router
from app.api.user import router as user_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(
    customer_router,
    prefix="/api"
)
app.include_router(
    user_router,
    prefix="/api"
)


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
