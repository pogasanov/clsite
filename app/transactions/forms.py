from django import forms
from django.forms import ModelForm

from transactions.models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['is_requester_principal', 'requester_review', 'date',
                  'amount', 'currency', 'requester_recommendation', 'proof_receipt']

    def __init__(self, *args, **kwargs):
        requester = kwargs.pop('requester')
        requestee = kwargs.pop('requestee')
        super().__init__(*args, **kwargs)

        self.instance.requester = requester
        self.instance.requestee = requestee
        if self.files:
            self.instance.is_proof_by_requester = True

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['amount'].widget.attrs['class'] = 'form-control col-md-4 mr-2'
        self.fields['currency'].widget.attrs['class'] = 'form-control col-md-4 mr-2'
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['requester_recommendation'].widget.attrs['placeholder'] = 'Optional'
        self.fields['requester_recommendation'].widget.attrs.update({'rows': '3'})

        self.fields['requester_review'].widget = forms.RadioSelect(choices=self.fields['requester_review'].choices)


class ConfirmTransactionForm(ModelForm):
    ACTION_CONFIRM = 'confirm'
    ACTION_DENY = 'deny'
    ACTION_CHOICES = (
        (ACTION_CONFIRM, 'Confirm'),
        (ACTION_DENY, 'Deny')
    )
    submit = forms.ChoiceField(choices=ACTION_CHOICES)

    class Meta:
        model = Transaction
        fields = ['requestee_review', 'requestee_recommendation', 'proof_receipt', 'submit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['requestee_recommendation'].widget.attrs['placeholder'] = 'Optional'
        self.fields['requestee_recommendation'].widget.attrs.update({'rows': '3'})

        self.fields['requestee_review'].widget = forms.RadioSelect(choices=self.fields['requestee_review'].choices)

    def save(self, commit=True):
        transaction = super().save(commit=False)

        transaction.is_confirmed = self.cleaned_data['submit'] == self.ACTION_CONFIRM

        if not transaction.is_confirmed:
            transaction.requestee_recommendation = None
            transaction.requestee_review = None
            transaction.proof_receipt = None
        else:
            transaction.is_proof_by_requester = True if self.files else None

        transaction.save()
