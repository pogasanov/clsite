from django.shortcuts import render, redirect

from .forms import RegistrationForm


def index(request):
    return render(request, "landing-page.html", context={})


def profile(request):
    return render(request, "profile-page.html", context={})


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "registration/registration.html", context={form: form})
