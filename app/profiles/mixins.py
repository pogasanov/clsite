from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def signup_flow_complete(function):
    EXCLUDED_PATHS = (
        reverse_lazy('profile'),
        reverse_lazy('profile-proof'),
    )

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.path not in EXCLUDED_PATHS and not request.user.is_anonymous:
            if not request.user.is_filled():
                messages.add_message(request, messages.ERROR, 'You should fill out profile')
                return HttpResponseRedirect(reverse_lazy('profile'))

            if not request.user.is_attorney_proof_submitted():
                messages.add_message(request, messages.ERROR, 'You should submit your attorney proof')
                return HttpResponseRedirect(reverse_lazy('profile-proof'))

        return function(request, *args, **kwargs)

    return wrap
