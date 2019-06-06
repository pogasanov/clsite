from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


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


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response
