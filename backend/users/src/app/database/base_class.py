from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.database.mixins import AllFeaturesMixin
from app.database.session import SessionScoped


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# We will need this for querying
Base.query = SessionScoped.query_property()

# Enhanced Base Model Class with some django-like super powers
class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True

    @classmethod
    def all_by_page(cls, page: int = 1, limit: int = 20, **kwargs) -> Dict:
        start = (page - 1) * limit
        end = start + limit
        return cls.query.slice(start, end).all()

    @classmethod
    def get(cls, **kwargs) -> Dict:
        """Return the the first value in database based on given args.
        Example:
            User.get(id=5)
        """
        return cls.where(**kwargs).first()


BaseModel.set_session(SessionScoped())