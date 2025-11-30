import graphene
from graphene_django import DjangoObjectType
from posts.models import Post
from user.schema import CustomUserType
from comments.schema import CommentType
from graphql_jwt.decorators import login_required


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("post_id", "content", "author", "created_at", "comments")

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, post_id=graphene.UUID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.all()
    
    def resolve_post_by_id(root, info, post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return None

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, content):
        author = info.context.user
        post = Post.objects.create(author=author, content=content)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.UUID(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id, content):
        author = info.context.user
        try:
            post = Post.objects.get(post_id=post_id, author=author)
            post.content = content
            post.save()
            return UpdatePost(post=post)
        except Post.DoesNotExist:
            raise Exception("Post not found or you're not the author")

class DeletePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        post_id = graphene.UUID(required=True)
    
    @login_required
    def mutate(self, info, post_id):
        author = info.context.user
        try:
            post = Post.objects.get(post_id=post_id, author=author)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            raise Exception("Post not found or you're not the author")

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)