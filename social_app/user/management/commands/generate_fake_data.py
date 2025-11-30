import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from interactions.models import Like, Repost
from follow.models import Follow

User = get_user_model()


class Command(BaseCommand):
    help = "Generate fake data for development/testing"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10, help="Number of users to create")
        parser.add_argument("--posts", type=int, default=50, help="Number of posts to create")
        parser.add_argument("--comments", type=int, default=100, help="Number of comments to create")
        parser.add_argument("--likes", type=int, default=200, help="Number of likes to create")
        parser.add_argument("--reposts", type=int, default=50, help="Number of reposts to create")
        parser.add_argument("--follows", type=int, default=30, help="Number of follows to create")
        parser.add_argument("--reset", action="store_true", help="Delete ALL generated data before creating new ones")

    def random_datetime(self, days_back=90):
        fake = Faker()
        end = timezone.now()
        start = end - timedelta(days=days_back)
        return fake.date_time_between(start_date=start, end_date=end, tzinfo=timezone.get_current_timezone())

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker()

        # =============================
        # RESET OPTION
        # =============================
        if options["reset"]:
            self.stdout.write("Deleting old fake data...")
            User.objects.exclude(is_superuser=True).delete()
            Like.objects.all().delete()
            Repost.objects.all().delete()
            Follow.objects.all().delete()
            Comment.objects.all().delete()
            Post.objects.all().delete()
            self.stdout.write(self.style.WARNING("All existing fake data deleted."))

        # =============================
        # CREATE USERS
        # =============================
        users = [
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"
            )
            for _ in range(options["users"])
        ]

        self.stdout.write(f"Created {len(users)} users.")

        # # =============================
        # # CREATE POSTS
        # # =============================
        posts = [
            Post.objects.create(
                content=fake.text(max_nb_chars=200),
                author=random.choice(users),
                created_at=self.random_datetime()
            )
            for _ in range(options["posts"])
        ]
        self.stdout.write(f"Created {len(posts)} posts.")

        # # =============================
        # # CREATE COMMENTS
        # # =============================
        comments = [
            Comment.objects.create(
                content=fake.sentence(),
                user=random.choice(users),
                post=random.choice(posts),
                created_at=self.random_datetime()
            )
            for _ in range(options["comments"])
        ]
        self.stdout.write(f"Created {len(comments)} comments.")

        # # =============================
        # # CREATE LIKES (unique)
        # # =============================
        like_set = set()
        likes_created = 0

        while likes_created < options["likes"]:
            user = random.choice(users)
            post = random.choice(posts)

            if (user, post) not in like_set:
                Like.objects.create(user=user, post=post)
                like_set.add((user, post))
                likes_created += 1

        self.stdout.write(f"Created {likes_created} likes.")

        # # =============================
        # # CREATE REPOSTS (unique)
        # # =============================
        repost_set = set()
        reposts_created = 0

        while reposts_created < options["reposts"]:
            user = random.choice(users)
            post = random.choice(posts)

            if (user, post) not in repost_set:
                Repost.objects.create(user=user, post=post)
                repost_set.add((user, post))
                reposts_created += 1

        self.stdout.write(f"Created {reposts_created} reposts.")

        # # =============================
        # # CREATE FOLLOWS (unique)
        # # =============================
        follow_set = set()
        follows_created = 0

        while follows_created < options["follows"]:
            follower = random.choice(users)
            following = random.choice(users)

            if follower != following and (follower, following) not in follow_set:
                Follow.objects.create(follower=follower, following=following)
                follow_set.add((follower, following))
                follows_created += 1

        self.stdout.write(f"Created {follows_created} follows.")

        self.stdout.write(self.style.SUCCESS("Fake data generation complete."))
