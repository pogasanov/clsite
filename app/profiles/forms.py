from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django_select2.forms import Select2TagWidget
from django.conf.global_settings import LANGUAGES

from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, _get_states_for_country
from .models import (Profile, Education, WorkExperience, Address, Admissions,
                     LawSchool, Organization, Award, Transaction, Jurisdiction)


DEFAULT_CHOICES_SELECTION = (('', '------'),)
DEFAULT_COUNTRY = 'United States of America'

class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)


class MultiSelectArrayFieldWidget(Select2TagWidget):
    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ",".join(values)

    def optgroups(self, name, value, attrs=None):
        value = value[0].split(',') if value else []
        return super().optgroups(name, value, attrs)


class DynamicMultiSelectArrayFieldWidget(MultiSelectArrayFieldWidget):
    """
    Allow user to create custom tags dynamically or user can select
    form existing predefined tags list
    """

    def optgroups(self, name, value, attrs=None):
        values = value[0].split(',') if value else []
        selected_values = set(filter(None, values))
        tags = super().optgroups(name, value, attrs)
        choices = set((item[0] for item in SUBJECTIVE_TAGS_CHOICES))
        custom_tags = selected_values - choices
        if custom_tags:
            custom_tag_items = [self.create_option(name, v, v, custom_tags, i)
                                for i, v in enumerate(custom_tags, len(choices))]
            tags.append((None, custom_tag_items, 0))

        selected_tags = []
        available_tags = []
        # To preserve the selected tags order on edit action
        for _, item, index in tags:
            tag_name = item[0]['value']
            if tag_name in values:
                selected_tags.append((None, item, values.index(tag_name)))
            else:
                available_tags.append((None, item, index+len(values)))
        # pre-append selected tags of into options
        options = sorted(selected_tags, key=lambda tag: tag[-1])
        options.extend(available_tags)
        return options


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ('first_name',
                  'last_name',
                  'headline',
                  'summary',
                  'experience',
                  'current_job',
                  'website',
                  'twitter',
                  'linkedin',
                  'facebook',
                  'phone',
                  'email',
                  'handle',
                  'preferred_communication_method',
                  'size_of_clients',
                  'license_status',
                  'languages',
                  'clients',
                  'law_type_tags',
                  'subjective_tags',
                  'bio',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'rows': '2'})
        self.fields['law_type_tags'].widget = MultiSelectArrayFieldWidget(
            choices=LAW_TYPE_TAGS_CHOICES, attrs={
                'data-tags': False, 'class': 'form-control'}
        )
        self.fields['subjective_tags'].widget = DynamicMultiSelectArrayFieldWidget(
            choices=SUBJECTIVE_TAGS_CHOICES, attrs={'class': 'form-control',
                                                    'data-maximum-selection-length': 3,
                                                    'data-token-separators': [',']}
        )
        self.fields['clients'].widget = MultiSelectArrayFieldWidget(
            attrs={'class': 'form-control', 'data-token-separators': [',']}
        )
        self.fields['languages'].widget = MultiSelectArrayFieldWidget(
            choices=LANGUAGES, attrs={
                'data-tags': False, 'class': 'form-control'}
        )

    def save(self, commit=True):
        updated_profile = super().save(commit=False)
        updated_profile.first_name = self.cleaned_data.get(
            'first_name', updated_profile.first_name)
        updated_profile.last_name = self.cleaned_data.get(
            'last_name', updated_profile.last_name)
        updated_profile.subjective_tags = list(map(str.capitalize, self.cleaned_data.get('subjective_tags')))
        updated_profile.save()
        return updated_profile


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key=='country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key=='state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


EducationFormSet = inlineformset_factory(Profile, Education,
                                         form=EducationForm, extra=1)


class AdmissionsForm(ModelForm):
    class Meta:
        model = Admissions
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key=='country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key=='state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})


AddmissionsFormSet = inlineformset_factory(Profile, Admissions,
                                           form=AdmissionsForm, extra=1)


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['responsibility'].widget.attrs.update({'rows': '2'})


WorkExperienceFormSet = inlineformset_factory(Profile, WorkExperience,
                                              form=WorkExperienceForm, extra=1)


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


OrganizationFormSet = inlineformset_factory(Profile, Organization,
                                            form=OrganizationForm, extra=1)


class AwardForm(ModelForm):
    class Meta:
        model = Award
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '2'})


AwardFormSet = inlineformset_factory(Profile, Award,
                                     form=AwardForm, extra=1)


class LawSchoolForm(ModelForm):
    class Meta:
        model = LawSchool
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key=='country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key=='state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['is_requester_principal', 'requester_review', 'date',
                  'amount', 'currency', 'requester_recommendation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_requester_principal'].widget = forms.NullBooleanSelect()
        self.fields['is_requester_principal'].widget.choices = (
            (True, "I paid them"),
            (False, "They paid me")
        )

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['amount'].widget.attrs['class'] = 'form-control col-md-4 mr-2'
        self.fields['currency'].widget.attrs['class'] = 'form-control col-md-4 mr-2'

        self.fields['is_requester_principal'].label = 'Did one of you pay the other?'
        self.fields['requester_recommendation'].label = 'Write a brief written recommendation'
        self.fields['requester_review'].label = 'Would you work with them again?'
        self.fields['date'].label = 'What was the date of the transaction?'
        self.fields['date'].widget.attrs['class'] += ' datepicker'

    def save(self, requester, requestee, commit=True):
        transaction = super().save(commit=False)
        transaction.requester = requester
        transaction.requestee = requestee

        if transaction.currency == 'USD':
            transaction.value_in_usd = transaction.amount

        transaction.save()
        return transaction


class JurisdictionForm(ModelForm):
    class Meta:
        model = Jurisdiction
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key=='country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key=='state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})


JurisdictionFormSet = inlineformset_factory(Profile, Jurisdiction,
                                         form=JurisdictionForm, extra=1)
