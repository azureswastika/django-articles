from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="user_img")
def media_folder_users(string):
    if not string:
        return f"{settings.STATIC_URL}img/user.png"
    return f"{settings.MEDIA_URL}{string}"
