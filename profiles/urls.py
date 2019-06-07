from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from clsite.settings import MEDIA_URL, MEDIA_ROOT
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('login', auth_views.LoginView.as_view(success_url='/'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.UserRegistrationView.as_view(), name='register'),

    path('profile', views.profile, name='profile'),
    path('profile/<username>', views.profile, name='profile'),

    path('users', views.UserListView.as_view(), name='users')
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


