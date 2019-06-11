from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'jurisdiction', 'headline', 'bio', 'website', 'twitter', 'linkedin', 'facebook']

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
