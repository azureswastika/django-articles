from django.db import models
from django.db.models import ForeignKey
from django.db.models.deletion import CASCADE
from django.db.models.fields import (
    BooleanField,
    DateTimeField,
    PositiveIntegerField,
    TextField,
)
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser


class Post(models.Model):
    user = ForeignKey(CustomUser, CASCADE)
    text = TextField(_("Текст"))
    likes = PositiveIntegerField(_("Количество лайков"), default=0)
    created_at = DateTimeField(_("Время публикации"), auto_now_add=True)
    is_active = BooleanField(default=True)
    likes = ManyToManyField(CustomUser, "likes", blank=True)

    class Meta:
        ordering = ("-created_at",)

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
