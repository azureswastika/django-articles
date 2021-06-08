from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="user_img")
def media_folder_users(string: str):
    if not string:
        return f"{settings.STATIC_URL}img/user.png"
    if str(string).startswith("http"):
        return string
    return f"{settings.MEDIA_URL}{string}"


@register.filter(name="is_follower")
def is_follower(user, another_user):
    return user.is_follower(another_user)


@register.filter(name="user_liked")
def user_liked(post, user):
    return post.user_liked(user)
