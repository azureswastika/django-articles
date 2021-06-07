from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, EmailField, ImageField
from django.db.models.fields import DateTimeField, PositiveIntegerField
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = CharField(
        _("имя пользователя"),
        max_length=55,
        unique=True,
        error_messages={
            "unique": _("Пользователь с таким именем уже зарегистрирован.")
        },
    )
    email = EmailField(
        _("электронный адрес"),
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": _("Пользователь с такой электронной почтой уже зарегистрирован.")
        },
    )
    image = ImageField(_("Фото профиля"), upload_to="profile/", null=True, blank=True)
    followers = ManyToManyField("users.CustomUser", "user_followers", blank=True)
    following = ManyToManyField("users.CustomUser", "user_following", blank=True)
    posts = PositiveIntegerField(_("Записи"), default=0)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    join_date = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        ordering = ("username", )

    def __str__(self) -> str:
        return self.username

    def get_followers_query(self):
        return self.followers.all()

    def get_following_query(self):
        return self.following.all()

    def get_posts(self):
        return (
            apps.get_app_config("articles")
            .get_model("Post")
            .objects.filter(user=self, is_active=True)
        )

    def is_follower(self, user):
        return self.followers.filter(pk=user.pk).exists()

    def get_url(self):
        return f"/user/{self.username}/"

    def get_followers_url(self):
        return f"/user/{self.username}/followers/"

    def get_following_url(self):
        return f"/user/{self.username}/following/"


@receiver(m2m_changed, sender=CustomUser.followers.through)
def followers_change(sender, instance: CustomUser, action: str, pk_set: set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            if instance.pk != pk:
                user = CustomUser.objects.get(pk=pk)
                user.following.add(instance)
    if action == "post_remove":
        for pk in pk_set:
            user = CustomUser.objects.get(pk=pk)
            user.following.remove(instance)
