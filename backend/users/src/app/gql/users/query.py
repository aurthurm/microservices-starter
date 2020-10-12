import graphene
from graphene import (
    relay,
    String,
)
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyConnectionField
from fastapi import Depends
from app.gql.users.types import UserType # noqa
from app.apps.user import crud, models # noqa

from sqlalchemy.orm import Session
from app.database.session import SessionScoped # noqa
from app.gql import deps # noqa

sync_db = SessionScoped.session_factory()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user_all = SQLAlchemyConnectionField(UserType.connection)
    user_me = graphene.Field(lambda: UserType, token=graphene.String(default_value=""))
    user_by_username = graphene.Field(lambda: UserType, username=graphene.String(default_value=""))
    user_by_email = graphene.Field(lambda: UserType, email=graphene.String(default_value=""))

    def resolve_user_me(self, info, token):
        """
        Get current user.
        """
        current_active_user = deps.get_current_active_user(token=token)
        return current_active_user

    def resolve_user_by_username(self, info, username, db: Session = sync_db):
        user = crud.user.get_by_username(db, username=username)
        return user

    def resolve_user_by_email(self, info, email, db: Session = sync_db):
        user = crud.user.get_by_email(db, email=email)
        return user


class AQuery(graphene.ObjectType):
    node = relay.Node.Field()
    user_all = SQLAlchemyConnectionField(UserType.connection)
    user_me = graphene.Field(lambda: UserType, token=graphene.String(default_value=""))
    user_by_username = graphene.Field(lambda: UserType, username=graphene.String(default_value=""))
    user_by_email = graphene.Field(lambda: UserType, email=graphene.String(default_value=""))

    def resolve_user_me(self, info, token):
        """
        Get current user.
        """
        current_active_user = deps.get_current_active_user(token=token)
        return current_active_user

    def resolve_user_by_username(self, info, username, db: Session = sync_db):
        user = crud.user.get_by_username(db, username=username)
        return user

    def resolve_user_by_email(self, info, email, db: Session = sync_db):
        user = crud.user.get_by_email(db, email=email)
        return user