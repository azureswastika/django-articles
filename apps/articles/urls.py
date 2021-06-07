from django.urls import path

from .views import FeedView, IndexView, RecommendationsView, like_post

app_name = "articles"

urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
    path("post/like/<int:post>", like_post, name="like_post"),
]
