from django.shortcuts import render


def index(request):
    return render(request, "landing-page.html", context={})


def profile(request):
    return render(request, "profile-page.html", context={})


def login(request):
    return render(request, "login-page.html", context={})
