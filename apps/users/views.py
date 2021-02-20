from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from apps.articles.models import Post
from apps.users.models import CustomUser, Follower

from .forms import LoginForm, RegisterForm


class RedirectAuthUser:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_redirect_url()
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class Login(RedirectAuthUser, LoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("articles:feed")

    def get_redirect_url(self) -> str:
        return self.success_url


class Register(RedirectAuthUser, CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("articles:login")

    def get_redirect_url(self) -> str:
        return self.success_url


class Logout(LogoutView):
    next_page = reverse_lazy("users:login")


class Profile(DetailView):
    model = CustomUser
    template_name = "users/profile.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get("username"):
            return self.request.user
        return get_object_or_404(CustomUser, is_active=True, *self.args, **self.kwargs)

    def get_context_data(self, *args, **kwargs):
        kwargs["posts"] = Post.get_user_posts(kwargs["object"])
        return super().get_context_data(*args, **kwargs)


class Followers(ListView):
    template_name = "users/followers.html"

    def get_queryset(self):
        if self.request.user.username == self.kwargs.get("username"):
            return Follower.get_followers(self.request.user)
        user = get_object_or_404(CustomUser, **self.kwargs)
        return Follower.get_followers(user)


class Following(ListView):
    template_name = "users/following.html"

    def get_queryset(self):
        if self.request.user.username == self.kwargs.get("username"):
            return Follower.get_following(self.request.user)
        user = get_object_or_404(CustomUser, **self.kwargs)
        return Follower.get_following(user)
