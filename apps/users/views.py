from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from apps.users.models import CustomUser

from .forms import LoginForm, RegisterForm


class RedirectAuthUser:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_redirect_url()
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class Login(RedirectAuthUser, LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('articles:root')

    def get_redirect_url(self) -> str:
        return self.success_url


class Register(RedirectAuthUser, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('articles:login')

    def get_redirect_url(self) -> str:
        return self.success_url


class Logout(LogoutView):
    next_page = reverse_lazy('articles:root')


class Profile(DeleteView):
    model = CustomUser
    template_name = 'users/user_profile.html'

    def get_object(self):
        return get_object_or_404(CustomUser, *self.args, **self.kwargs)
