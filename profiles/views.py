from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm


def index(request):
    return render(request, "landing-page.html", context={})


@login_required
def profile(request):
    return render(request, "profile-page.html", context={
        'user': request.user
    })


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "registration/registration.html", context={form: form})
