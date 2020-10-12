from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay
from app.apps.user.models import User # noqa

# Graphene User Type
class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )