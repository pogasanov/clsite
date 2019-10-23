from django.shortcuts import render

from profiles.mixins import profile_filled


@profile_filled
def home(request):
    return render(request, 'pages/home.html')
