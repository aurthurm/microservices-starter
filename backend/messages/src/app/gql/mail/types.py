from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay
from app.apps.mail.models import EMail # noqa

# Graphene Email Type
class MailType(SQLAlchemyObjectType):
    class Meta:
        model = EMail
        interfaces = (relay.Node, )