from django.urls import path

from .views import FeedView, IndexView, like_post

app_name = "articles"

urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("post/like/<int:post>", like_post, name="like_post")
]
