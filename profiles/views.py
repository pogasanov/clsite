from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import ListView

from .forms import RegistrationForm


def index(request):
    return render(request, "landing-page.html", context={})


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(get_user_model(), username=username)
    else:
        user = request.user
    return render(request, "profile-page.html", context={
        'selected_user': user
    })


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "registration/registration.html", context={form: form})


class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['id']
