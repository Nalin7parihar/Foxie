from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser:
    def get(self, db: Session, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = db.execute(stmt)
        return list(result.scalars().all())

    def get_by_username(self, db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=hashed_password,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> User | None:
        db_user = self.get(db, id)
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user


user = CRUDUser()
