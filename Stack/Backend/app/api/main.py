from fastapi import FastAPI

from app.api import customer

app = FastAPI(
    title="Insurance CRM API"
)

app.include_router(
    customer.router,
    prefix="/api"
)


@app.get("/")
def root():
    return {"message": "Insurance CRM API is running"}