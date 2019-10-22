from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from profiles.forms import ProfileCreationForm


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response
