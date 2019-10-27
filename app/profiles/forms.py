from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory
from django.utils.safestring import mark_safe
from django_select2.forms import Select2TagWidget

from clsite.settings import DEFAULT_CHOICES_SELECTION, DEFAULT_COUNTRY
from .models import (Profile, Education, WorkExperience, Address, Admissions,
                     LawSchool, Organization, Award, Jurisdiction, Language)
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, _get_states_for_country, \
    CUSTOM_SORTED_LANGUAGES_CHOICES


def unique_field_formset(*fields):
    from django.forms.models import BaseInlineFormSet
    class UniqueFieldFormSet(BaseInlineFormSet):
        def clean(self):
            if any(self.errors):
                return  # Ignore if form has errors already
            formset_values = set()
            for form in self.forms:
                values = []
                for field in fields:
                    if form.cleaned_data.get(field): values.append(form.cleaned_data.get(field))
                form_values = '-'.join(values)  # Make a values string for quick check

                if form_values in formset_values:
                    form.add_error('__all__', 'Duplicate values.')
                formset_values.add(form_values)

    return UniqueFieldFormSet


class ProfileCreationForm(UserCreationForm):
    agree_tos = forms.BooleanField(label=mark_safe(
        'I agree to the <a href="/privacy-terms-and-conditions" _target="blank">Terms and Conditions</a>'))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('full_name', 'email', 'password1', 'password2', 'agree_tos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['agree_tos'].widget.attrs['class'] = 'form-check-input'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full name...'
        self.fields['email'].widget.attrs['placeholder'] = 'Email...'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password...'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password...'


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
                available_tags.append((None, item, index + len(values)))
        # pre-append selected tags of into options
        options = sorted(selected_tags, key=lambda tag: tag[-1])
        options.extend(available_tags)
        return options


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name',
                  'summary',
                  'experience',
                  'current_job',
                  'website',
                  'twitter',
                  'linkedin',
                  'facebook',
                  'phone',
                  'email',
                  'preferred_communication_method',
                  'size_of_clients',
                  'law_type_tags',
                  'subjective_tags',
                  'bio',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def save(self, commit=True):
        updated_profile = super().save(commit=False)
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
            if key == 'country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key == 'state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['state'].label = 'State/Province'


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
            if key == 'country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key == 'state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['state'].label = 'State/Province'


AdmissionsFormSet = inlineformset_factory(Profile, Admissions,
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
            if key == 'country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key == 'state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['state'].label = 'State/Province'


class JurisdictionForm(ModelForm):
    class Meta:
        model = Jurisdiction
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'country':
                field.widget.attrs.update({'class': 'form-control country'})
                field.initial = DEFAULT_COUNTRY
            elif key == 'state':
                field.widget = forms.Select(attrs={'class': 'form-control'})
                field.widget.choices = DEFAULT_CHOICES_SELECTION + _get_states_for_country(DEFAULT_COUNTRY)
            else:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['state'].label = 'State/Province'


JurisdictionFormSet = inlineformset_factory(Profile, Jurisdiction,
                                            formset=unique_field_formset('country', 'state', 'city'),
                                            form=JurisdictionForm, extra=1, min_num=1, validate_min=True)


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].choices = CUSTOM_SORTED_LANGUAGES_CHOICES
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


LanguageFormSet = inlineformset_factory(Profile, Language, formset=unique_field_formset('name'), form=LanguageForm,
                                        extra=0)


class ProfileProofForm(ModelForm):
    attorney_confirm = forms.BooleanField(required=True,
                                          label='I affirm, under penalty of perjury, that I am a licensed attorney.')

    class Meta:
        model = Profile
        fields = ('passport_photo', 'bar_license_photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['passport_photo'].required = True
        self.fields['bar_license_photo'].required = True
