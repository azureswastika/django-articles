from django.http import request
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


class RecommendationsView(RedirectNotAuthUser, ListView):
    template_name = "articles/recommendations.html"
    context_object_name = "posts"

    def get_queryset(self):
        liked = Post.objects.filter(likes=self.request.user)[:5]
        posts = []
        for like in liked:
            for user in like.likes.all().exclude(pk=self.request.user.pk):
                for post in Post.objects.filter(likes=user).exclude(likes__pk=self.request.user.pk)[:5]:
                    posts.append(post)
        return sorted(list(set(posts)), key=lambda post: post.created_at)[::-1]


def like_post(request, post):
    post = get_object_or_404(Post, pk=post)
    if post.user_liked(request.user):
        post.likes.remove(request.user)
        return JsonResponse({"liked": False, "count": f"{post.likes.count()}"})
    post.likes.add(request.user)
    return JsonResponse({"liked": True, "count": f"{post.likes.count()}"})
