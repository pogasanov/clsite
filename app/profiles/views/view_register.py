from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from profiles.forms import ProfileCreationForm
from profiles.mixins import signup_flow_complete
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


@method_decorator(signup_flow_complete, name='dispatch')
class ProfileProofView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('passport_photo', 'bar_license_photo')
    template_name = 'profiles/profile_proof.html'

    def get_object(self, queryset=None):
        self.previous_object_status = self.request.user.register_status
        return self.request.user

    def get_success_url(self):
        if self.previous_object_status == Profile.REGISTER_STATUS_NO_ATTORNEY_PROOF:
            if self.object.register_status == Profile.REGISTER_STATUS_COMPLETE:
                return reverse('profile-signup-flow-completed')
            if self.object.register_status == Profile.REGISTER_STATUS_EMAIL_NOT_CONFIRMED:
                return reverse('profile-email-confirmation')
        return reverse('profile-proof')



@login_required
def profile_email_confirmation_view(request):
    if request.user.email_confirmed_at:
        return redirect(reverse('profile'))
    return render(request, 'profiles/profile_email_confirmation.html')


@login_required
def profile_signup_flow_complteted_view(request):
    return render(request, 'profiles/signup_flow_completed.html')
