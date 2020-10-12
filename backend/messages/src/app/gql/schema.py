import graphene
from graphene import String
from graphql import GraphQLError

from app.apps.mail import schemas, models # noqa
from app.gql.mail import query as mail_query # noqa
from app.gql.mail import mutations as mail_mutations # noqa

class Query(
    mail_query.Query, 
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(graphene.ObjectType):
    mailcreate = mail_mutations.CreateEMail.Field()
    

gql_schema = graphene.Schema(query=Query, mutation=Mutation)