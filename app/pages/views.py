from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')


def privacy_terms_conditions_view(request):
    return HttpResponse()
