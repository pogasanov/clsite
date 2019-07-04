from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View

from .forms import ProfileForm, EducationFormSet, WorkExperienceFormSet, AddressForm, AddmissionsFormSet, LawSchoolForm, \
    OrganizationFormSet, AwardFormSet, ProfileCreationForm

from .choices import USA_STATES
from .lawtypetags.utilities import LAW_TYPE_TAGS_CHOICES, get_all_tags_flat_list

def index(request):
    return render(request, "landing-page.html", context={})


@login_required
def profile(request, handle=None):
    if handle:
        user = get_object_or_404(get_user_model(), handle=handle)
        profile_form = None
        address_form = None
        education_formset = None
        admissions_formset = None
        lawschool_form = None
        workexperience_formset = None
        organization_formset = None
        award_formset = None
    else:
        user = request.user
        profile_form = ProfileForm(request.POST or None, instance=user, prefix='profile')
        address_form = AddressForm(request.POST or None, instance=getattr(user, 'address', None), prefix='address')
        education_formset = EducationFormSet(request.POST or None, instance=user, prefix='education')
        admissions_formset = AddmissionsFormSet(request.POST or None, instance=user, prefix='admissions')
        lawschool_form = LawSchoolForm(request.POST or None, instance=getattr(user, 'lawschool', None), prefix='lawschool')
        workexperience_formset = WorkExperienceFormSet(request.POST or None, instance=user, prefix='workexperience')
        organization_formset = OrganizationFormSet(request.POST or None, instance=user, prefix='organization')
        award_formset = AwardFormSet(request.POST or None, instance=user, prefix='award')

        if request.method == 'POST':
            if request.FILES.get('photo-input'):
                url = update_user_profile_photo(user, request.FILES['photo-input'])
                return JsonResponse({'url': url})
            else:
                if profile_form.is_valid() and \
                        address_form.is_valid() and \
                        education_formset.is_valid() and \
                        admissions_formset.is_valid() and \
                        lawschool_form.is_valid() and \
                        workexperience_formset.is_valid() and \
                        organization_formset.is_valid() and \
                        award_formset.is_valid():
                    profile_form.save()
                    af = address_form.save(commit=False)
                    af.profile = user
                    af.save()
                    education_formset.instance = user
                    education_formset.save()
                    admissions_formset.instance = user
                    admissions_formset.save()
                    lf = lawschool_form.save(commit=False)
                    lf.profile = user
                    lf.save()
                    workexperience_formset.instance = user
                    workexperience_formset.save()
                    organization_formset.instance = user
                    organization_formset.save()
                    award_formset.instance = user
                    award_formset.save()
                    return JsonResponse({'message': 'Your data has been updated successfully!'})
                else:
                    errors = {
                        'profile': profile_form.errors,
                        'address': address_form.errors,
                        'education': education_formset.errors,
                        'admissions': admissions_formset.errors,
                        'lawschool': lawschool_form.errors,
                        'workexperience': workexperience_formset.errors,
                        'organization': organization_formset.errors,
                        'award': award_formset.errors,
                        'message': 'Invalid data provided!'
                    }
                    return JsonResponse(errors, status=400)

    return render(request, "profile-page.html", context={
        'selected_user': user,
        'form': profile_form,
        'address': address_form,
        'educations': education_formset,
        'admissions': admissions_formset,
        'lawschool': lawschool_form,
        'workexperiences': workexperience_formset,
        'organizations': organization_formset,
        'awards': award_formset
    })


def update_user_profile_photo(user, photo):
    if user.photo:
        # remove previous photo
        photo_storage = user.photo.storage
        previous_photo = user.photo.name
        if photo_storage.exists(previous_photo):
            photo_storage.delete(previous_photo)

    user.photo = photo
    user.save()

    return user.photo.url


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['id']



class ProfileBrowsingView(View):
    template_name = 'profile-browsing.html'
    # form_class = ProfileCreationForm
    # success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        list_jurisdictions = [state[1] for state in USA_STATES]
        list_law_type_tags = get_all_tags_flat_list(LAW_TYPE_TAGS_CHOICES)
        return render(request, self.template_name, {'jurisdictions': list_jurisdictions})

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if self.object:
    #         login(request, self.object)
    #     return response