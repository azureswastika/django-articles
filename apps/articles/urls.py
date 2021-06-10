from django.urls import path

from .views import (
    ArchiveView,
    FeedView,
    IndexView,
    RecommendationsView,
    delete_post,
    like_post,
)

app_name = "articles"

urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("archive/", ArchiveView.as_view(), name="archive"),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
    path("post/<int:post>/like/", like_post, name="like_post"),
    path("post/<int:post>/delete/", delete_post, name="delete_post"),
]
