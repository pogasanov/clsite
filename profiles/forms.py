from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'jurisdiction', 'headline', 'website', 'twitter', 'linkedin', 'facebook','bio']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['jurisdiction'].widget.attrs.update({'class': 'form-control jurisdiction-field'})
        self.fields['headline'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['twitter'].widget.attrs.update({'class': 'form-control'})
        self.fields['linkedin'].widget.attrs.update({'class': 'form-control'})
        self.fields['facebook'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'rows': '2'})

    def save(self, commit=True):
        updated_profile = super(ProfileForm, self).save(commit=False)
        updated_profile.user.first_name = self.cleaned_data.get('first_name', updated_profile.user.first_name)
        updated_profile.user.last_name = self.cleaned_data.get('last_name', updated_profile.user.last_name)
        updated_profile.save()
        updated_profile.user.save()
        return updated_profile
