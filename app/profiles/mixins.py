from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect


def profile_filled(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            if not request.user.is_filled():
                messages.add_message(request, messages.ERROR, 'You should fill out profile')
                return HttpResponseRedirect('/profile')

            if not request.user.is_attorney_proof_submitted():
                messages.add_message(request, messages.ERROR, 'You should submit your attorney proof')
                return HttpResponseRedirect('/profile/proof')

        return function(request, *args, **kwargs)

    return wrap
