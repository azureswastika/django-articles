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
