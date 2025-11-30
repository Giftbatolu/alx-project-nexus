import graphene
from graphene_django import DjangoObjectType
from follow.models import Follow
from user.schema import CustomUserType
from graphql_jwt.decorators import login_required


class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")


class Query(graphene.ObjectType):
    followers = graphene.List(CustomUserType, user_id=graphene.ID(required=True))
    following = graphene.List(CustomUserType, user_id=graphene.ID(required=True))

    @login_required
    def resolve_followers(root, info, user_id):
        return [
            follow.follower
            for follow in Follow.objects.filter(following_id=user_id)
        ]

    @login_required
    def resolve_following(root, info, user_id):
        return [
            follow.following
            for follow in Follow.objects.filter(follower_id=user_id)
        ]



class FollowUser(graphene.Mutation):
    success = graphene.Boolean()
    follow = graphene.Field(FollowType)

    class Arguments:
        user_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, user_id):
        follower = info.context.user
        if follower.id == int(user_id):
            raise Exception("You cannot follow yourself")

        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following_id=user_id
        )
        return FollowUser(success=True, follow=follow)


class UnfollowUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        user_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, user_id):
        follower = info.context.user
        try:
            follow = Follow.objects.get(
                follower=follower,
                following_id=user_id
            )
            follow.delete()
            return UnfollowUser(success=True)
        except Follow.DoesNotExist:
            raise Exception("You are not following this user")


class Mutation(graphene.ObjectType):
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)