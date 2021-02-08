from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import BooleanField, CharField, EmailField, ImageField
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = CharField(
        _('имя пользователя'),
        max_length=55,
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким именем уже зарегистрирован.')})
    email = EmailField(
        _('электронный адрес'),
        unique=True,
        null=True,
        blank=True,
        error_messages={
            'unique': _('Пользователь с такой электронной почтой уже зарегистрирован.')})
    image = ImageField(_('Фото профиля'), upload_to="profile/", null=True, blank=True)
    followers = PositiveIntegerField(_('Подписчики'), default=0)
    following = PositiveIntegerField(_('Подписки'), default=0)
    posts = PositiveIntegerField(_('Записи'), default=0)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    join_date = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    def get_url(self):
        return f'/user/{self.username}/'

    def get_followers_url(self):
        return f'/user/{self.username}/followers/'

    def get_following_url(self):
        return f'/user/{self.username}/following/'


class Follower(models.Model):
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    following = ForeignKey(CustomUser, on_delete=CASCADE, related_name='user')

    def __str__(self) -> str:
        return f'`{self.user}` подписан на `{self.following}`'

    def save(self, *args, **kwargs):
        try:
            if self.user != self.following:
                Follower.objects.get(user=self.user, following=self.following)
            return
        except ObjectDoesNotExist:
            if self.pk is None:
                self.user.following += 1
                self.user.save()
                self.following.followers += 1
                self.following.save()
            return super().save(*args, **kwargs)
        else:
            return

    def delete(self, *args, **kwargs):
        self.user.following -= 1
        self.user.save()
        self.following.followers -= 1
        self.following.save()
        return super().delete(*args, **kwargs)

    @staticmethod
    def get_followers(user):
        return Follower.objects.filter(following=user)

    @staticmethod
    def get_following(user):
        return Follower.objects.filter(user=user)
