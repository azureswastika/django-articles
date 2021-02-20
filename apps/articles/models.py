from datetime import datetime

from django.db import models
from django.db.models import ForeignKey
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, DateTimeField, TextField
from django.utils.translation import gettext_lazy as _

from apps.users import CustomUser


class Post(models.Model):
    user = ForeignKey(CustomUser, CASCADE)
    text = TextField(_("Текст"))
    created_at = DateTimeField(_("Время публикации"), default=datetime.now())
    is_active = BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.text[:30]} ({self.user})"

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:
            self.user.posts += 1
        elif self.is_active:
            self.user.posts += 1
        else:
            self.user.posts -= 1
        self.user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.posts -= 1
        self.user.save()
        self.is_active = False
        self.save()
        return

    @staticmethod
    def get_user_posts(user):
        return Post.objects.filter(user=user, is_active=True).order_by("-created_at")
