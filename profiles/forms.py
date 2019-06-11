from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'jurisdiction', 'headline', 'bio', 'website', 'twitter', 'linkedin', 'facebook']
