from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import os
from django.contrib.auth.mixins import LoginRequiredMixin
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
        if request.method == 'POST' and request.FILES['photo-input']:
            previous_photo = user.profile.photo
            user.profile.photo = request.FILES['photo-input']
            user.profile.save()

            # remove previous photo
            if previous_photo.url.split('/')[2] != "dummy-img.png":
                os.remove(previous_photo.url[1:])

            return JsonResponse({'url': user.profile.photo.url})
    return render(request, "profile-page.html", context={
        'selected_user': user
    })


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "registration/registration.html", context={form: form})


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['id']
