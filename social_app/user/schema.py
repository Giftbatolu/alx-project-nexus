import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "profile_picture")

class Query(graphene.ObjectType):
    me = graphene.Field(CustomUserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return user

class RegisterUser(graphene.Mutation):
    user = graphene.Field(lambda: CustomUserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        if User.objects.filter(username=username).exists():
            return RegisterUser(success=False, errors=["Username already exists"])
        if User.objects.filter(email=email).exists():
            return RegisterUser(success=False, errors=["Email already exists"])

        user = User.objects.create_user(username=username, email=email, password=password)

        return RegisterUser(user=user, success=True, errors=None)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register_user = RegisterUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)