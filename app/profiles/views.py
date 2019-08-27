from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from itertools import groupby

from .forms import ProfileForm, EducationFormSet, WorkExperienceFormSet, AddressForm, AdmissionsFormSet, LawSchoolForm, \
    OrganizationFormSet, AwardFormSet, ProfileCreationForm, TransactionForm, JurisdictionFormSet, ConfirmTransactionForm, \
    LanguageFormSet
from .models import Profile, Transaction, Jurisdiction
from .utils import _get_states_for_country
from .helpers import get_user_relationships
from clsite.settings import DEFAULT_CHOICES_SELECTION


def index(request):
    return render(request, "landing-page.html", context={})


def user_relationships(user):
    user_relations = get_user_relationships(user)
    # User with highest cumulative verified transactions amount first and so on. Secondly sorted by highest amount
    sorted_user_relationships = sorted(
        user_relations.items(),
        key=lambda x: (
            sum([t.value_in_usd or 0 for t in x[1] if t.is_verified]),
            sum([t.value_in_usd or 0 for t in x[1]])
        ),
        reverse=True
    )
    relationships = []

    for user_handle, transactions in sorted_user_relationships:
        relationship = {}

        other_user = get_object_or_404(get_user_model(), handle=user_handle)
        relationship['name'] = other_user.full_name
        relationship['url'] = reverse('profile', args=[other_user.handle])
        relationship['photo'] = other_user.photo_url_or_default()

        relationship['verified_amount']= sum([t.value_in_usd or 0 for t in transactions if t.is_verified])
        relationship['unverified_amount'] = sum([t.value_in_usd or 0 for t in transactions if not t.is_verified])

        amount_given = 0
        amount_given += sum([t.value_in_usd or 0 for t in transactions if t.requester == user and t.is_requester_principal])
        amount_given += sum([t.value_in_usd or 0 for t in transactions if t.requestee == user and not t.is_requester_principal])
        relationship['amount_given'] = amount_given

        amount_received = 0
        amount_received += sum([t.value_in_usd or 0 for t in transactions if t.requester == user and not t.is_requester_principal])
        amount_received += sum([t.value_in_usd or 0 for t in transactions if t.requestee == user and t.is_requester_principal])
        relationship['amount_received'] = amount_received

        relationship['jurisdiction']= [str(j) for j in other_user.jurisdiction_set.all()]
        relationship['law_type_tags'] = other_user.law_type_tags or []

        if not amount_given and not amount_received:
            continue

        relationships.append(relationship)

    return relationships


@login_required
def get_states(request, handle=None):
    if request.method == 'POST':
        country = request.POST.get('country')
        if country:
            states = DEFAULT_CHOICES_SELECTION + _get_states_for_country(country)
            return JsonResponse({'data': states})
        else:
            pass
        return JsonResponse({'data': []})


@login_required
def profile(request, handle=None):
    if handle:
        user = get_object_or_404(get_user_model(), handle=handle)
        profile_form = None
        jurisdiction_formset = None
        address_form = None
        education_formset = None
        admissions_formset = None
        lawschool_form = None
        workexperience_formset = None
        organization_formset = None
        award_formset = None
        language_formset = None
    else:
        user = request.user
        profile_form = ProfileForm(request.POST or None, instance=user, prefix='profile')
        jurisdiction_formset = JurisdictionFormSet(request.POST or None, instance=user, prefix='jurisdiction')
        address_form = AddressForm(request.POST or None, instance=getattr(user, 'address', None), prefix='address')
        education_formset = EducationFormSet(request.POST or None, instance=user, prefix='education')
        admissions_formset = AdmissionsFormSet(request.POST or None, instance=user, prefix='admissions')
        lawschool_form = LawSchoolForm(request.POST or None, instance=getattr(user, 'lawschool', None), prefix='lawschool')
        workexperience_formset = WorkExperienceFormSet(request.POST or None, instance=user, prefix='workexperience')
        organization_formset = OrganizationFormSet(request.POST or None, instance=user, prefix='organization')
        award_formset = AwardFormSet(request.POST or None, instance=user, prefix='award')
        language_formset = LanguageFormSet(request.POST or None, instance=user, prefix='language')

        if request.method == 'POST':
            if request.FILES.get('photo-input'):
                url = update_user_profile_photo(user, request.FILES['photo-input'])
                return JsonResponse({'url': url})
            else:
                if profile_form.is_valid() and \
                        jurisdiction_formset.is_valid() and \
                        address_form.is_valid() and \
                        education_formset.is_valid() and \
                        admissions_formset.is_valid() and \
                        lawschool_form.is_valid() and \
                        workexperience_formset.is_valid() and \
                        organization_formset.is_valid() and \
                        award_formset.is_valid() and \
                        language_formset.is_valid():
                    profile_form.save()
                    jurisdiction_formset.instance = user
                    jurisdiction_formset.save()
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
                    language_formset.instance = user
                    language_formset.save()
                    return JsonResponse({'message': 'Your data has been updated successfully!'})
                else:
                    errors = {
                        'profile': profile_form.errors,
                        'jurisdiction': jurisdiction_formset.errors,
                        'address': address_form.errors,
                        'education': education_formset.errors,
                        'admissions': admissions_formset.errors,
                        'lawschool': lawschool_form.errors,
                        'workexperience': workexperience_formset.errors,
                        'organization': organization_formset.errors,
                        'award': award_formset.errors,
                        'language': language_formset.errors,
                        'message': 'Invalid data provided!'
                    }
                    return JsonResponse(errors, status=400)

    return render(request, "profile-page.html", context={
        'selected_user': user,
        'form': profile_form,
        'jurisdiction': jurisdiction_formset,
        'address': address_form,
        'educations': education_formset,
        'admissions': admissions_formset,
        'lawschool': lawschool_form,
        'workexperiences': workexperience_formset,
        'organizations': organization_formset,
        'awards': award_formset,
        'languages': language_formset,
        'relationships': user_relationships(user)[:5] if handle else None
    })

@login_required
def transaction(request, handle):
    user = request.user
    receiver = get_object_or_404(get_user_model(), handle=handle)

    if user == receiver:
        return HttpResponseBadRequest()

    transaction_form = TransactionForm(request.POST or None)

    if transaction_form.is_valid():
        transaction_form.save(requester=user, requestee=receiver)
        messages.info(
            request,
            "Thank you. We have contacted {} to confirm the transaction with the following details.".format(receiver.full_name.upper()),
        )
        return redirect('home')

    return render(request, "transaction.html", context={'form': transaction_form})

@login_required
def confirm_transaction(request, transaction_id):
    user = request.user
    user_transaction = get_object_or_404(Transaction, id=transaction_id)

    if user_transaction != user.user_unconfirmed_transaction():
        return HttpResponseBadRequest()

    form = ConfirmTransactionForm(request.POST or None, initial={'requestee_review': 'N'}, instance=user_transaction)

    if request.POST and form.is_valid():
        is_confirmed = request.POST['submit'] != 'deny'
        form.save(is_confirmed=is_confirmed)

        return redirect('home')

    context = {
        'transaction': user_transaction,
        'form': form
    }

    return render(request, "confirm_transaction.html", context=context)


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

    def get_tuple_display_from_value(self, search_tuple, list_values=[]):
        display_list = []
        for value in list_values:
            if dict(search_tuple).get(value):
                display_list.append(dict(search_tuple)[value])
        return display_list

    def get_flat_tags_and_usage(self, profiles_law_type_tags):
        flat_law_tags = []
        for profile in profiles_law_type_tags:
            if profile.law_type_tags:
                flat_law_tags.extend(profile.law_type_tags)

        law_tags_with_occurrence = [{"name": tag, "occurrence": len(list(group))} for tag, group in groupby(sorted(flat_law_tags))]
        return sorted(law_tags_with_occurrence, key=lambda k: k['occurrence'], reverse=True)

    def get(self, request, *args, **kwargs):
        list_users = Profile.objects.all()
        profiles_law_type_tags = list_users.only('law_type_tags')
        usage_list_law_type_tags = self.get_flat_tags_and_usage(profiles_law_type_tags)

        list_jurisdictions = Jurisdiction.objects.exclude(state=None).values_list('state', flat=True)  # gets only non-null states entries
        usage_list_jurisdictions = [{"name": tag, "occurrence": len(list(group))} for tag, group in groupby(sorted(list_jurisdictions))]
        usage_list_jurisdictions = sorted(usage_list_jurisdictions, key=lambda k: k['occurrence'], reverse=True)

        return render(request, self.template_name, {'jurisdictions': usage_list_jurisdictions,
                                                    'law_type_tags': usage_list_law_type_tags,
                                                    'users': list_users})


class BrowsingView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'browsing.html'
    ordering = ['id']

    def get_tuple_key_from_value(self, tuple=(), value=None):
        for row in tuple:
            if row[1] == value:
                return row[0]
        return None

    def get_tuple_value_from_key(self, tuple=(), value=None):
        for row in tuple:
            if row[0] == value:
                return row[1]
        return None

    def get_unique_options(self, list_values):
        unique_list = []
        for row in list_values:
            if row:
                unique_list = list(set(unique_list) | set(row))
        return unique_list

    def get(self, request, *args, **kwargs):
        list_users = Profile.objects.all()
        jurisdiction = kwargs.get('jurisdiction_value') if kwargs.get('jurisdiction_value') != 'all' else None
        law_tags_value = kwargs.get('law_tags_value') if kwargs.get('law_tags_value') != 'all' else None
        law_tags_list = None
        jurisdiction_list = None
        if jurisdiction:
            list_users = list_users.filter(jurisdiction__state=jurisdiction)
            law_tags_list = self.get_unique_options(list_users.values_list('law_type_tags', flat=True))
        if law_tags_value:
            list_users = list_users.filter(law_type_tags__contains=[law_tags_value])
            list_users_ids = list(list_users.values_list(flat=True).distinct())
            jurisdiction_list = list(Jurisdiction.objects.filter(profile_id__in=list_users_ids).values_list('state', flat=True).distinct())
        return render(request, self.template_name, {'users': list_users, 'jurisdiction_list': jurisdiction_list, 'law_tags_list': law_tags_list})