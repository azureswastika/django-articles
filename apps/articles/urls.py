from django.urls import path

from .views import FeedView, IndexView

app_name = "articles"

urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("feed/", FeedView.as_view(), name="feed"),
]
