from django.urls import path

from .views import (
    FollowersView,
    FollowingView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
    validate_email,
    validate_username,
    validate_password,
)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("user/<str:username>/", ProfileView.as_view(), name="profile"),
    path("user/<str:username>/followers/", FollowersView.as_view(), name="followers"),
    path("user/<str:username>/following/", FollowingView.as_view(), name="following"),
    path("validate_email/", validate_email, name="validate_email"),
    path("validate_username/", validate_username, name="validate_username"),
    path("validate_password/", validate_password, name="validate_password"),
]
