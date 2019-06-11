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
        updated_user = super(ProfileForm, self).save(commit=False)
        updated_user.profile.jurisdiction = self.cleaned_data.get('jurisdiction', updated_user.profile.jurisdiction)
        updated_user.profile.headline = self.cleaned_data.get('headline', updated_user.profile.headline)
        updated_user.profile.bio = self.cleaned_data.get('bio', updated_user.profile.bio)
        updated_user.profile.website = self.cleaned_data.get('website', updated_user.profile.website)
        updated_user.profile.twitter = self.cleaned_data.get('twitter', updated_user.profile.twitter)
        updated_user.profile.linkedin = self.cleaned_data.get('linkedin', updated_user.profile.linkedin)
        updated_user.profile.facebook = self.cleaned_data.get('facebook', updated_user.profile.facebook)
        updated_user.profile.save()
        updated_user.save()
        return updated_user
