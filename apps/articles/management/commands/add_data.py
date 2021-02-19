from random import randint, choice

from apps.articles.models import Post
from apps.users.models import CustomUser, Follower
from django.core.management.base import BaseCommand
from requests import get


class Command(BaseCommand):
    help = "Add users/articles"

    def handle(self, *args, **options):
        try:
            CustomUser.objects.create_superuser(
                username="admin", email="admin@mail.com", password="root"
            )
        except Exception:
            pass
        users = get(
            "https://randomuser.me/api/?results="
            "{}&exc=gender,name,location,dob,registered,id,phone,cell,nat".format(
                options["users"]
            )
        ).json()["results"]
        for user in users:
            email = user["email"]
            username = user["login"]["username"]
            image = user["picture"]["large"]
            try:
                user = CustomUser.objects.create_user(
                    username=username, email=email, password="root", image=image, is_active=True
                )
            except Exception:
                pass
            else:
                for i in range(randint(3, 15)):
                    text = get("https://loripsum.net/api/1/plaintext").text.strip()
                    Post.objects.create(user=user, text=text)
        users = CustomUser.objects.all()
        for user in users:
            for i in range(randint(1, 20)):
                Follower.objects.create(user=choice(users), following=user)

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--users",
            default="20",
        )
