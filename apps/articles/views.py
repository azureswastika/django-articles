from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView

from apps.articles.models import Post
from apps.users.models import Follower


class RedirectNotAuthUser:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(request.path)
        return super().dispatch(request, *args, **kwargs)


class Feed(RedirectNotAuthUser, ListView):
    template_name = "articles/feed.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        followers = Follower.objects.filter(user=self.request.user).values_list(
            "following"
        )
        return Post.objects.filter(user__in=followers).order_by("-created_at")
