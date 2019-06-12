from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['first_name',
                  'last_name',
                  'address',
                  'jurisdiction',
                  'headline',
                  'education',
                  'website',
                  'twitter',
                  'linkedin',
                  'facebook',
                  'phone',
                  'experience',
                  'email',
                  'current_job',
                  'size_of_clients',
                  'preferred_communication_method',
                  'license_status',
                  'languages',
                  'law_school',
                  'work_experiences',
                  'associations',
                  'clients',
                  'awards',
                  'bio',
                  ]

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
