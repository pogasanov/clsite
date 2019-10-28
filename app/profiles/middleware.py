from django.conf import settings
from django.contrib.auth.decorators import login_required

from profiles.mixins import signup_flow_complete


class InternalPagesMiddleware:
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path in settings.PUBLIC_PAGES:
            return view_func(request, *view_args, **view_kwargs)
        signup_flow_complete_decorated = signup_flow_complete(view_func)
        login_required_decorated = login_required(signup_flow_complete_decorated)
        return login_required_decorated(request, *view_args, **view_kwargs)
