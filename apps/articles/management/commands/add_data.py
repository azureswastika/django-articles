import random
from datetime import datetime, timedelta
from random import choice, randint

import pytz
from apps.articles.models import Post
from apps.users.models import CustomUser, Follower
from django.core.management.base import BaseCommand
from requests import get


def add_posts(users):
    for user in users:
        for i in range(randint(3, 15)):
            text = get("https://loripsum.net/api/1/plaintext").text.strip()
            Post.objects.create(user=user, text=text, created_at=gen_datetime())
            print("Пользователь: {}\nСоздан пост: {}".format(user, text))


def gen_datetime(min_year=2019, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00, tzinfo=pytz.UTC)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def add_followers(users):
    for following in users:
        for i in range(randint(1, 20)):
            user = choice(users)
            Follower.objects.create(user=user, following=following)
            print("{} подписался на {}".format(following, user))


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
        add_posts(users)
        add_followers(users)

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--users",
            default="20",
        )
