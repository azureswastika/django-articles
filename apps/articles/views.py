from django.http.response import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from apps.articles.mixins import RedirectNotAuthUser
from django.shortcuts import get_object_or_404
from .models import Post


class IndexView(TemplateView):
    template_name = "articles/index.html"


class FeedView(RedirectNotAuthUser, ListView):
    template_name = "articles/feed.html"
    context_object_name = "posts"
    # paginate_by = 10

    def get_queryset(self):
        return self.request.user.get_feed()


class RecommendationsView(RedirectNotAuthUser, ListView):
    template_name = "articles/recommendations.html"
    context_object_name = "posts"

    def get_queryset(self):
        return self.request.user.get_recommendations()


def like_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return JsonResponse(post.like(request.user))
