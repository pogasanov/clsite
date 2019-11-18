from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from profiles.models import Profile


class ProfileCreationForm(UserCreationForm):
    agree_tos = forms.BooleanField(
        label=mark_safe(
            'I agree to the <a href="/privacy-terms-and-conditions" _target="blank">Terms and Conditions</a>'
        )
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("full_name", "email", "password1", "password2", "agree_tos")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["agree_tos"].widget.attrs["class"] = "form-check-input"
        self.fields["full_name"].widget.attrs["placeholder"] = "Full name..."
        self.fields["email"].widget.attrs["placeholder"] = "Email..."
        self.fields["password1"].widget.attrs["placeholder"] = "Password..."
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat password..."


class ProfileProofForm(ModelForm):
    attorney_confirm = forms.BooleanField(
        required=True, label="I affirm, under penalty of perjury, that I am a licensed attorney."
    )

    class Meta:
        model = Profile
        fields = ("passport_photo", "bar_license_photo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["passport_photo"].required = True
        self.fields["bar_license_photo"].required = True
