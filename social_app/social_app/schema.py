import graphene
from posts import schema as posts_schema
from user import schema as user_schema
from comments import schema as comments_schema

class Query(
    posts_schema.Query,
    user_schema.Query,
    graphene.ObjectType
    ):
    pass

class Mutation(
    posts_schema.Mutation,
    user_schema.Mutation,
    comments_schema.Mutation,
    graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)