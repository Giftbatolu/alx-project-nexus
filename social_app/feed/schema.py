import graphene
from graphene_django import DjangoObjectType
from posts.schema import PostType
from follow.models import Follow
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    feed = graphene.List(PostType)

    @login_required
    def resolve_feed(root, info):
        user = info.context.user

        following_ids = Follow.objects.filter(
            follower=user
        ).values_list("following_id", flat=True)

        return Post.objects.filter(
            author__in=following_ids
        ).order_by("-created_at")

schema = graphene.Schema(query=Query)