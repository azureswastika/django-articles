from django.urls import path

from .views import Login, Logout, Profile, Register

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('user/<slug:username>/', Profile.as_view(), name='profile'),
]
