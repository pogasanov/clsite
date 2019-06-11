from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


def index(request):
    return render(request, "landing-page.html", context={})


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(get_user_model(), username=username)
    else:
        user = request.user
        if request.method == 'POST' and request.FILES['photo-input']:
            photo_storage = user.profile.photo.storage
            # remove previous photo
            previous_photo = user.profile.photo.name
            if photo_storage.exists(previous_photo) and previous_photo != "dummy-img.png":
                photo_storage.delete(previous_photo)

            user.profile.photo = request.FILES['photo-input']
            user.profile.save()

            return JsonResponse({'url': user.profile.photo.url})
    return render(request, "profile-page.html", context={
        'selected_user': user
    })


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['id']
