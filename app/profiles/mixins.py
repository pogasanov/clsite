from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from profiles.models import Profile


def signup_flow_complete(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            if request.path != reverse('profile') \
                    and request.user.register_status == Profile.REGISTER_STATUS_EMPTY_PROFILE:
                messages.add_message(request, messages.ERROR, 'You should fill out profile')
                return HttpResponseRedirect(reverse('profile'))

            if request.path != reverse('profile-proof'):
                if request.user.register_status == Profile.REGISTER_STATUS_NO_ATTORNEY_PROOF:
                    messages.add_message(request, messages.ERROR, 'You should submit your attorney proof')
                    return HttpResponseRedirect(reverse('profile-proof'))

                if request.path != reverse('profile-email-confirmation') \
                        and request.user.register_status == Profile.REGISTER_STATUS_EMAIL_NOT_CONFIRMED:
                    return HttpResponseRedirect(reverse('profile-email-confirmation'))

        return function(request, *args, **kwargs)

    return wrap
