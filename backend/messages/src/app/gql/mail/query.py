import graphene
from graphene import (
    relay,
    String,
)
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyConnectionField
from fastapi import Depends
from app.gql.mail.types import MailType # noqa
from app.apps.mail import crud, models # noqa

from sqlalchemy.orm import Session
from app.database.session import SessionScoped # noqa
from app.gql import deps # noqa

sync_db = SessionScoped.session_factory()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    mails_all = SQLAlchemyConnectionField(MailType.connection)
    mails_by_sender = graphene.Field(lambda: MailType, token=graphene.String(default_value=""))

    def resolve_mails_all(self, info, token):
        """
        Get all mails.
        """
        
        return {}

    def resolve_mails_by_sender(self, info, username, db: Session = sync_db):
        
        return {}

