from django.views.generic import TemplateView
from django.views.generic.list import ListView

from apps.articles.mixins import RedirectNotAuthUser
from apps.users.models import Follower

from .models import Post


class IndexView(TemplateView):
    template_name = "articles/index.html"


class FeedView(RedirectNotAuthUser, ListView):
    template_name = "articles/feed.html"
    context_object_name = "posts"
    # paginate_by = 10

    def get_queryset(self):
        followers = Follower.objects.filter(user=self.request.user).values_list(
            "following"
        )
        return Post.objects.filter(user__in=followers).order_by("-created_at")
