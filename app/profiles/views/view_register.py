from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from profiles.forms import ProfileCreationForm
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


class ProfileProofView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('email',)
    template_name = 'profiles/profile_proof.html'

    def get_object(self, queryset=None):
        return self.request.user
