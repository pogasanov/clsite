from django.shortcuts import render

from profiles.mixins import signup_flow_complete


@signup_flow_complete
def home(request):
    return render(request, 'pages/home.html')
