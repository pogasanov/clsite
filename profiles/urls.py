from django.urls import path, reverse_lazy
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
    path('register', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url=reverse_lazy('login')
    ), name='register'),

    path('profile', views.profile, name='profile'),
    path('profile/<username>', views.profile, name='profile'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
