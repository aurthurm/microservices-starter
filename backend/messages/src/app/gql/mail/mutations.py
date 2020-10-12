from datetime import timedelta
from fastapi.encoders import jsonable_encoder
import graphene
from graphql import GraphQLError
from sqlalchemy.orm import Session
from app.core.config import settings # noqa
from app.apps.mail.utils import ( # noqa
    send_new_account_email,
)
from app.apps.mail import crud, schemas # noqa
from app.gql.mail.types import MailType # noqa


from app.database.session import SessionScoped # noqa
from app.database.session import database as async_db # noqa

sync_db = SessionScoped.session_factory()


class CreateEMail(graphene.Mutation):
    class Arguments:
        sender = graphene.String(required=True)
        subject = graphene.String(required=True)
        body = graphene.String(required=True)
        cc = graphene.String(required=True)
        token = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, token, sender, subject, body, cc, db: Session = sync_db, ):
        ok = True
        return CreateEMail(ok=ok)
