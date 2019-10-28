from django.conf import settings
from django.contrib.auth.decorators import login_required

from profiles.mixins import signup_flow_complete


class InternalPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in settings.PUBLIC_PAGES:
            return self.get_response(request)

        signup_flow_complete_decorated = signup_flow_complete(self.get_response)
        login_required_decorated = login_required(signup_flow_complete_decorated)
        return login_required_decorated(request)
