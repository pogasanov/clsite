from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from clsite.settings import MEDIA_URL, MEDIA_ROOT
from .views import views, view_register

urlpatterns = \
    [
        path('login', auth_views.LoginView.as_view(success_url='/'), name='login'),
        path('logout', auth_views.LogoutView.as_view(), name='logout'),
        path('register', view_register.UserRegistrationView.as_view(), name='register'),

        path('profile', views.profile, name='profile'),
        path('profile/proof', view_register.ProfileProofView.as_view(), name='profile-proof'),
        path('profile/email', view_register.profile_email_confirmation_view, name='profile-email-confirmation'),
        path('profile/complete', view_register.profile_signup_flow_complteted_view,
             name='profile-signup-flow-completed'),
        path('profile/<handle>', views.ProfileDetailView.as_view(), name='profile-detail'),

        path('profiles', views.UserListView.as_view(), name='profiles'),
        path('profiles/jurisdictions/<jurisdiction_value>/law-type-tags/<law_tags_value>',
             views.BrowsingView.as_view(), name='profiles-browsing'),

        path('states', views.get_states, name='states'),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
