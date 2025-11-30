import graphene
from graphene_django import DjangoObjectType
from comments.models import Comment
from user.schema import CustomUserType

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("comment_id", "post", "user", "content", "created_at", "comments")

class WriteComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.UUID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        comment = Comment.objects.create(
            post_id=post_id,
            user=user,
            content=content
        )
        return WriteComment(comment=comment)

class UpdateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        comment_id = graphene.UUID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, comment_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        try:
            comment = Comment.objects.get(comment_id=comment_id, user=user)
            comment.content = content
            comment.save()
            return UpdateComment(comment=comment)
        except Comment.DoesNotExist:
            raise Exception("Comment not found or you're not the author")

class DeleteComment(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        comment_id = graphene.UUID(required=True)
    
    def mutate(self, info, comment_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        try:
            comment = Comment.objects.get(comment_id=comment_id, user=user)
            comment.delete()
            return DeleteComment(success=True)
        except Comment.DoesNotExist:
            raise Exception("Comment not found or you're not the author")

class Mutation(graphene.ObjectType):
    write_comment = WriteComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()

schema = graphene.Schema(mutation=Mutation)