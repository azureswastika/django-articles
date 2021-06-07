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
        return Post.get_feed(self.request.user)


def like_post(request, post):
    post = get_object_or_404(Post, pk=post)
    if post.user_liked(request.user):
        post.likes.remove(request.user)
        return JsonResponse({"liked": False, "count": f"{post.likes.count()}"})
    post.likes.add(request.user)
    return JsonResponse({"liked": True, "count": f"{post.likes.count()}"})
