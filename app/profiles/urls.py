from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers

from clsite.settings import MEDIA_URL, MEDIA_ROOT
from profiles.views import ProfileViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet)

urlpatterns = \
    [
        path('login', auth_views.LoginView.as_view(success_url='/'), name='login'),
        path('logout', auth_views.LogoutView.as_view(), name='logout'),
        path('register', views.UserRegistrationView.as_view(), name='register'),

        path('profile', views.profile, name='profile'),
        path('profile/<handle>', views.ProfileDetailView.as_view(), name='profile-detail'),

        path('profiles', views.UserListView.as_view(), name='profiles'),
        path('profiles/jurisdictions/<jurisdiction_value>/law-type-tags/<law_tags_value>',
             views.BrowsingView.as_view(), name='profiles-browsing'),

        path('states', views.get_states, name='states'),
        path('', include(router.urls))
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
