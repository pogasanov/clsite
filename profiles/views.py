from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
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


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['id']
