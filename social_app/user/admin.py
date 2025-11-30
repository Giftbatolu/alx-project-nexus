from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from posts.models import Post
from comments.models import Comment
from follow.models import Follow
from interactions.models import Like, Repost

User = get_user_model()

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("username", "email", "is_staff", "is_active")
#     search_fields = ("username", "email")
#     list_filter = ("is_staff", "is_active")

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Repost)