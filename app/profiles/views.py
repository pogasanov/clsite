from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from itertools import groupby

from .forms import ProfileForm, EducationFormSet, WorkExperienceFormSet, AddressForm, AddmissionsFormSet, LawSchoolForm, \
    OrganizationFormSet, AwardFormSet, ProfileCreationForm
from .models import Profile
from .choices import USA_STATES


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

    def get_tuple_key_from_value(self, tuple=(), value=None):
        for row in tuple:
            if row[1] == value:
                return row[0]
        return None

    def get_tuple_display_from_value(self, search_tuple, list_values=[]):
        display_list = []
        for value in list_values:
            if dict(search_tuple).get(value):
                display_list.append(dict(search_tuple)[value])
        return display_list

    def get_flat_tags_and_usage(self, profiles_law_type_tags):
        flat_law_tags = []
        flat_jurisdictions = []
        for profile in profiles_law_type_tags:
            if profile.law_type_tags:
                flat_law_tags.extend(profile.law_type_tags)
            if profile.jurisdiction:
                flat_jurisdictions.extend(self.get_tuple_display_from_value(USA_STATES, profile.jurisdiction))

        law_tags_with_occurrence = [{"name": tag, "occurrence": len(list(group))} for tag, group in groupby(sorted(flat_law_tags))]
        jurisdiction_with_occurrence = [
            {"name": jurisdiction, "occurrence": len(list(group))} for jurisdiction, group in groupby(sorted(flat_jurisdictions))
        ]

        return sorted(law_tags_with_occurrence, key=lambda k: k['occurrence'], reverse=True), \
               sorted(jurisdiction_with_occurrence, key=lambda k: k['occurrence'], reverse=True)

    def get(self, request, *args, **kwargs):
        list_users = Profile.objects.all()
        profiles_law_type_tags = list_users.only('law_type_tags', 'jurisdiction')
        list_law_type_tags, list_jurisdictions = self.get_flat_tags_and_usage(profiles_law_type_tags)
        return render(request, self.template_name, {'jurisdictions': list_jurisdictions,
                                                    'law_type_tags': list_law_type_tags,
                                                    'users': list_users})

    def post(self, request, *args, **kwargs):
        list_users = []
        selected_jurisdiction = request.POST.get('jurisdiction')
        selected_law_tag = request.POST.get('law_type_tag')
        if selected_jurisdiction:
            jurisdiction_value = self.get_tuple_key_from_value(USA_STATES, selected_jurisdiction)
            profiles = Profile.objects.filter(jurisdiction__contains=[jurisdiction_value])
        elif selected_law_tag:
            profiles = Profile.objects.filter(law_type_tags__contains=[selected_law_tag])
        else:
            return JsonResponse({"users": list_users, "message": "Invalid Request"}, status=400)

        for match in profiles:
            profile_json ={
                'first_name': match.first_name,
                'last_name': match.last_name,
                'handle': match.handle,
                'headline': match.headline,
                'photo_url_or_default': match.photo_url_or_default()
            }
            list_users.append(profile_json)
        return JsonResponse({ "users": list(list_users)}, status=200)
