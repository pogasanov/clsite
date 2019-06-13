from django.forms import ModelForm, inlineformset_factory
from django import forms

from .models import Profile, Education, WorkExperience, Address, Admissions, LawSchool, Organization, Award


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ('first_name',
                  'last_name',
                  'headline',
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
                  'license_status',
                  'languages',
                  'clients',
                  'jurisdiction',
                  'bio',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'rows': '2'})

    def save(self, commit=True):
        updated_profile = super().save(commit=False)
        updated_profile.user.first_name = self.cleaned_data.get('first_name', updated_profile.user.first_name)
        updated_profile.user.last_name = self.cleaned_data.get('last_name', updated_profile.user.last_name)
        updated_profile.user.save()
        updated_profile.save()
        return updated_profile


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
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
            field.widget.attrs.update({'class': 'form-control'})
