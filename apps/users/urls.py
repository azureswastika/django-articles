from django.urls import path

from .views import Followers, Following, Login, Logout, Profile, Register

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('user/<str:username>/', Profile.as_view(), name='profile'),
    path('user/<str:username>/followers/', Followers.as_view(), name='followers'),
    path('user/<str:username>/following/', Following.as_view(), name='following'),
]
