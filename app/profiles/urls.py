from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from clsite.settings import MEDIA_URL, MEDIA_ROOT

from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('login', auth_views.LoginView.as_view(success_url='/'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.UserRegistrationView.as_view(), name='register'),

    path('profile', views.profile, name='profile'),
    path('profile/<handle>', views.profile, name='profile'),
    path('browsing', views.ProfileBrowsingView.as_view(), name='browsing'),

    path('users', views.UserListView.as_view(), name='users')
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


