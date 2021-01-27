from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, EmailField, ImageField
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
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
