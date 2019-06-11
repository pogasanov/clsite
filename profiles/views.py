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
from .forms import ProfileForm


def index(request):
    return render(request, "landing-page.html", context={})


@login_required
def profile(request, username=None):
    profile_form = None
    if username:
        user = get_object_or_404(get_user_model(), username=username)
    else:
        user = request.user
        if request.method == 'POST':
            if request.FILES.get('photo-input'):
                previous_photo = user.profile.photo
                user.profile.photo = request.FILES['photo-input']
                user.profile.save()

                # remove previous photo
                if previous_photo.url.split('/')[2] != "dummy-img.png":
                    os.remove(previous_photo.url[1:])

                return JsonResponse({'url': user.profile.photo.url})
            else:
                user.profile.headline = request.POST.get('headline') if request.POST.get('headline') else user.profile.headline
                user.profile.jurisdiction = request.POST.get('jurisdiction') if request.POST.get('jurisdiction') else user.profile.jurisdiction
                user.profile.website = request.POST.get('website') if request.POST.get('website') else user.profile.website
                user.profile.twitter = request.POST.get('twitter') if request.POST.get('twitter') else user.profile.twitter
                user.profile.linkedin = request.POST.get('linkedin') if request.POST.get('linkedin') else user.profile.linkedin
                user.profile.facebook = request.POST.get('facebook') if request.POST.get('facebook') else user.profile.facebook
                user.profile.bio = request.POST.get('bio') if request.POST.get('bio') else user.profile.bio
                user.save()

        profile_form = ProfileForm(initial=user.profile.__dict__)
    return render(request, "profile-page.html", context={
        'selected_user': user,
        'form': profile_form
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
