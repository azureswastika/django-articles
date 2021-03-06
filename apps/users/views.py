from django.contrib.auth.password_validation import (
    validate_password as ValidatePassword,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as ValidateEmail
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from apps.articles.forms import PostCreate
from apps.articles.models import Post
from apps.users.mixins import RedirectAuthUser
from apps.users.models import CustomUser, Follower

from .forms import LoginForm, RegisterForm


class LoginView(RedirectAuthUser, LoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("articles:feed")

    def get_redirect_url(self) -> str:
        return self.success_url


class RegisterView(RedirectAuthUser, CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("articles:login")

    def get_redirect_url(self) -> str:
        return self.success_url


class LogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


class ProfileView(DetailView, FormView):
    model = CustomUser
    form_class = PostCreate
    template_name = "users/profile.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get("username"):
            return self.request.user
        return get_object_or_404(CustomUser, is_active=True, *self.args, **self.kwargs)

    def get_context_data(self, *args, **kwargs):
        kwargs["posts"] = Post.get_user_posts(kwargs["object"])
        return super().get_context_data(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        Post.objects.create(user=request.user, text=form.data.get("text"))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse(
            "users:profile", kwargs={"username": self.kwargs.get("username")}
        )


class FollowersView(ListView):
    template_name = "users/followers.html"

    def get_queryset(self):
        if self.request.user.username == self.kwargs.get("username"):
            return Follower.get_followers(self.request.user)
        user = get_object_or_404(CustomUser, **self.kwargs)
        return Follower.get_followers(user)


class FollowingView(ListView):
    template_name = "users/following.html"

    def get_queryset(self):
        if self.request.user.username == self.kwargs.get("username"):
            return Follower.get_following(self.request.user)
        user = get_object_or_404(CustomUser, **self.kwargs)
        return Follower.get_following(user)


def validate_email(request):
    try:
        email = request.GET.get("email", None)
        ValidateEmail(email)
    except ValidationError:
        return JsonResponse({"is_taken": True})
    else:
        response = {"is_taken": CustomUser.objects.filter(email__iexact=email).exists()}
        return JsonResponse(response)


def validate_username(request):
    username = request.GET.get("username", None)
    response = {
        "is_taken": CustomUser.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_password(request):
    try:
        password = request.GET.get("password1", None)
        ValidatePassword(password)
        return JsonResponse({"valid": True})
    except (ValidationError, TypeError):
        return JsonResponse({"valid": False})
