from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from profiles.forms import ProfileCreationForm
from profiles.mixins import profile_filled
from profiles.models import Profile


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


@method_decorator(profile_filled, name='dispatch')
class ProfileProofView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('passport_photo', 'bar_license_photo')
    template_name = 'profiles/profile_proof.html'

    def get_object(self, queryset=None):
        return self.request.user
