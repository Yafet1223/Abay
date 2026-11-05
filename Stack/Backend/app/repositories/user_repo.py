from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create a user
    def create(self, user_data: UserCreate, hashed_password: str) -> User:

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # Get user by ID
    def get_by_id(self, user_id: int) -> User | None:

        statement = select(User).where(
            User.id == user_id
        )

        return self.db.scalar(statement)

    # Get user by email
    def get_by_email(self, email: str) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    # Get all users
    def get_all(self) -> list[User]:

        statement = select(User)

        return list(self.db.scalars(statement).all())

    # Update user
    def update(
        self,
        user: User,
        user_data: UserUpdate
    ) -> User:

        update_data = user_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    # Deactivate user
    def deactivate(self, user: User) -> User:

        user.is_active = False

        self.db.commit()
        self.db.refresh(user)

        return user