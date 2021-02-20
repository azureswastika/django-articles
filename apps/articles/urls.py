from django.urls import path
from django.views.generic import TemplateView

from .views import Feed

app_name = "articles"

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="root"),
    path("feed/", Feed.as_view(), name="feed"),
]
