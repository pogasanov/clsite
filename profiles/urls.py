from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('login', auth_views.LoginView.as_view(success_url='/'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.UserRegistrationView.as_view(), name='register'),

    path('profile', views.profile, name='profile'),
    path('profile/<username>', views.profile, name='profile'),
]
