from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def signup_flow_complete(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous and request.path != reverse('profile'):
            if not request.user.is_filled():
                messages.add_message(request, messages.ERROR, 'You should fill out profile')
                return HttpResponseRedirect(reverse('profile'))

            if request.path != reverse('profile-proof'):
                if not request.user.is_attorney_proof_submitted():
                    messages.add_message(request, messages.ERROR, 'You should submit your attorney proof')
                    return HttpResponseRedirect(reverse('profile-proof'))

                if not request.user.email_confirmed_at:
                    return HttpResponseRedirect(reverse('profile-email-confirmation'))

        return function(request, *args, **kwargs)

    return wrap
