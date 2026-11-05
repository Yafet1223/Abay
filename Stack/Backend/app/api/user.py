

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create a user
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)

    # Check if email already exists
    existing_user = user_repo.get_by_email(user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Password hashing will be added when we implement authentication.
    # Never save a raw password in the database.
    raise HTTPException(
        status_code=501,
        detail="User creation is not implemented yet. Password hashing is required."
    )


# Get all users
@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)

    return user_repo.get_all()


# Get user by ID
@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)

    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# Update user
@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)

    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_repo.update(user, user_data)


# Deactivate user
@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)

    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_repo.deactivate(user)
