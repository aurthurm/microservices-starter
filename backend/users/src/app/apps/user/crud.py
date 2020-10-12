from typing import Any, Dict, Optional, Union, TypeVar

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password # noqa
from app.apps.core.crud import CRUDBase, ACRUDBase
from .models import User
from .schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.user_name == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            user_name=obj_in.user_name,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def authenticate_by_username(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)


# ASYNC
import databases 
Database = TypeVar("Database", bound=databases.Database)

class ACRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Database, *, email: str) -> Optional[User]:
        query = self.table.select().where(self.model.email == email)
        return await db.fetch_one(query)
    
    async def get_by_username(self, db: Database, *, username: str) -> Optional[User]:
        query = self.table.select().where(self.model.username == username)
        return await db.fetch_one(query)

    async def create(self, db: Database, *, obj_in: UserCreate) -> User:
        obj_update = {
            "email": obj_in.email,
            "user_name": obj_in.user_name,
            "hashed_password": get_password_hash(obj_in.password),
            "first_name": obj_in.first_name,
            "last_name": obj_in.last_name,
            "is_superuser": obj_in.is_superuser,
        }
        query = self.table.insert().values(**obj_update)
        return await db.execute(query)

    async def update(
        self, db: Database, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: Database, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return await user

    async def authenticate_by_username(self, db: Database, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return await user

    async def is_active(self, user: User) -> bool:
        return await user.is_active

    async def is_superuser(self, user: User) -> bool:
        return await user.is_superuser
    
auser = ACRUDUser(User)