from django.urls import path

from .views import FeedView, IndexView, RecommendationsView, delete_post, like_post

app_name = "articles"

urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
    path("post/<int:post>/like/", like_post, name="like_post"),
    path("post/<int:post>/delete/", delete_post, name="delete_post")
]
