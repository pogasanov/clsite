from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect


def profile_filled(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_filled():
            messages.add_message(request, messages.ERROR, 'You should fill out profile')
            return HttpResponseRedirect('/profile')
        return function(request, *args, **kwargs)

    return wrap
