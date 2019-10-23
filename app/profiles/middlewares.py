from django.http import HttpResponseRedirect


class ProfileFilledMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != '/profile' \
                and hasattr(request, 'user') \
                and not request.user.is_anonymous \
                and not request.user.is_filled():
            return HttpResponseRedirect('/profile')
        response = self.get_response(request)
        return response
