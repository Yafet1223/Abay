
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.session import engine


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
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
