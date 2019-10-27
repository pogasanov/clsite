from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-terms-and-conditions', views.privacy_terms_conditions_view, name='privacy-terms-and-conditions'),
]
