from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # TODO: REMOVEME?
    path('', views.index, name='home'),
]
