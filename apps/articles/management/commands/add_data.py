from random import choices, randint

from apps.articles.models import Post
from apps.users.models import CustomUser
from django.core.management.base import BaseCommand
from lorem import get_paragraph
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
                    username=username,
                    email=email,
                    password="root",
                    image=image,
                    is_active=True,
                )
                print("Создан пользователь: {}".format(user))
            except Exception:
                pass
        users = CustomUser.objects.all()
        add_followers(users, users.count())
        add_posts(users)

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--users",
            default="20",
        )


def add_followers(users: list, users_count: int):
    for user in users:
        followers = choices(users, k=randint(1, users_count))
        user.followers.add(*followers)
        print(
            "{} подписались на {}".format(
                ", ".join(str(user) for user in followers), user
            )
        )


def add_posts(users):
    for user in users:
        print("Пользователь: {}".format(user))
        for i in range(randint(3, 15)):
            text = get_paragraph(randint(1, 2))
            post = Post.objects.create(user=user, text=text)
            likes = choices(users, k=randint(3, 12))
            post.likes.add(*likes)
            print("{} лайкнули {}".format(", ".join(str(user) for user in likes), post))
