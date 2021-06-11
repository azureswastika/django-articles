from django.http.response import JsonResponse
from django.views.generic import TemplateView, DetailView
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


class ArchiveView(RedirectNotAuthUser, ListView):
    template_name = "articles/recommendations.html"
    context_object_name = "posts"

    def get_queryset(self):
        return self.request.user.get_archive()


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = context["object"].get_comments()
        return context


def delete_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return JsonResponse({"deleted": post.archivate(request.user)})


def like_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return JsonResponse(post.like(request.user))
