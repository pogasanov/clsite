from django.shortcuts import render


def home(request):
    return render(request, 'pages/landing-page.html')
