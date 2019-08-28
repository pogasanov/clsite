from django import forms
from django.forms import ModelForm

from transactions.models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['is_requester_principal', 'requester_review', 'date',
                  'amount', 'currency', 'requester_recommendation', 'proof_receipt']

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
        self.fields['requester_recommendation'].widget.attrs['placeholder'] = 'Optional'
        self.fields['requester_recommendation'].widget.attrs.update({'rows': '3'})
        self.fields['requester_review'].widget = forms.RadioSelect(choices=self.fields['requester_review'].choices)

        self.fields['is_requester_principal'].label = 'Did one of you pay the other?'
        self.fields['proof_receipt'].label = 'Screenshot of wire transfer (Optional)'
        self.fields['requester_recommendation'].label = 'Write a brief recommendation'
        self.fields['requester_review'].label = 'Would you work with them again?'
        self.fields['date'].label = 'What was the date of the transaction?'
        self.fields['date'].widget.attrs['class'] += ' datepicker'

    def save(self, requester, requestee, is_proof_by_requester=None, commit=True):
        transaction = super().save(commit=False)
        transaction.requester = requester
        transaction.requestee = requestee
        transaction.is_proof_by_requester = is_proof_by_requester

        if transaction.currency == 'USD':
            transaction.value_in_usd = transaction.amount

        transaction.save()
        return transaction


class ConfirmTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['requestee_review', 'requestee_recommendation', 'proof_receipt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['requestee_review'].widget = forms.RadioSelect(choices=self.fields['requestee_review'].choices)
        self.fields['proof_receipt'].label = 'Screenshot of wire transfer (Optional)'
        self.fields['requestee_recommendation'].label = 'Write a brief recommendation'
        self.fields['requestee_recommendation'].widget.attrs['placeholder'] = 'Optional'
        self.fields['requestee_recommendation'].widget.attrs.update({'rows': '3'})
        self.fields['requestee_review'].label = 'Would you work with them again?'

    def save(self, is_confirmed, is_proof_by_requester=None, commit=True):
        transaction = super().save(commit=False)

        if not is_confirmed:
            transaction.requestee_recommendation = None
            transaction.requestee_review = None
            transaction.proof_receipt = None
        else:
            transaction.is_proof_by_requester = is_proof_by_requester
        transaction.is_confirmed = is_confirmed
        transaction.save()
