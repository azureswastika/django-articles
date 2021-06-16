from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView

from apps.articles.mixins import RedirectNotAuthUser
from django.shortcuts import get_object_or_404
from .models import Comment, Post


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

    def get_context_data(self, *args, **kwargs):
        kwargs["comments"] = kwargs["object"].get_comments()
        return super().get_context_data(*args, **kwargs)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Comment.objects.create(
            post=post, user=request.user, text=request.POST.get("text")
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("articles:post", kwargs={"pk": self.kwargs.get("pk")})


def delete_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return JsonResponse({"deleted": post.archivate(request.user)})


def like_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return JsonResponse(post.like(request.user))
