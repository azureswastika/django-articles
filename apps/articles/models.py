from django.db import models
from django.db.models import ForeignKey
from django.db.models.deletion import CASCADE
from django.db.models.fields import (
    BooleanField,
    DateTimeField,
    TextField,
)
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser


class Post(models.Model):
    user = ForeignKey(CustomUser, CASCADE)
    text = TextField(_("Текст"))
    likes = ManyToManyField(CustomUser, "likes", blank=True)
    created_at = DateTimeField(_("Время публикации"), auto_now_add=True)
    is_active = BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.text[:30]} ({self.user})"

    def delete(self, *args, **kwargs):
        self.is_active = not self.is_active
        self.save()
        return

    def like(self, user) -> dict:
        if self.user_liked(user):
            self.likes.remove(user)
            return {"liked": False, "count": self.likes.count()}
        self.likes.add(user)
        return {"liked": True, "count": self.likes.count()}

    def user_liked(self, user):
        return self.likes.filter(pk=user.pk).exists()

    def archivate(self, user) -> dict:
        if self.user != user:
            return None
        self.delete()
        return False if self.is_active else True

    @staticmethod
    def get_user_posts(user):
        return Post.objects.filter(user=user, is_active=True)
