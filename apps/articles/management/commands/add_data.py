from random import choice, randint
from threading import Thread

from apps.articles.models import Post
from apps.users.models import CustomUser, Follower
from django.core.management.base import BaseCommand
from requests import get


class Command(BaseCommand):
    help = "Add users/articles"

    def handle(self, *args, **options):
        def add_posts(users):
            for user in users:
                for i in range(randint(3, 15)):
                    text = get("https://loripsum.net/api/1/plaintext").text.strip()
                    Post.objects.create(user=user, text=text)
                    print("Пользователь: {}\nСоздан пост: {}".format(user, text))

        def add_followers(users):
            for following in users:
                for i in range(randint(1, 20)):
                    user = choice(users)
                    Follower.objects.create(user=user, following=following)
                    print("{} подписался на {}".format(following, user))

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
        posts = Thread(target=add_posts, args=[users])
        followers = Thread(target=add_followers, args=[users])
        posts.start()
        followers.start()

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--users",
            default="20",
        )
