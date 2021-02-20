from apps.articles.mixins import RedirectNotAuthUser
from django.views.generic.list import ListView

from apps.articles import Post
from apps.users import Follower


class Feed(RedirectNotAuthUser, ListView):
    template_name = "articles/feed.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        followers = Follower.objects.filter(user=self.request.user).values_list(
            "following"
        )
        return Post.objects.filter(user__in=followers).order_by("-created_at")
