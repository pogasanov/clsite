from django.shortcuts import render

from django.http import HttpResponse

from account.decorators import login_required

@login_required
def index(request):
    return render(request, "profiles.html", context={})
