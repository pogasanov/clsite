from django import forms
from django.forms import ModelForm

from transactions.models import Transaction


class TransactionForm(ModelForm):
    IS_REQUESTER_PRINCIPAL_CHOICES = (
        (Transaction.IS_REQUESTER_PRINCIPAL_YES, 'I paid them'),
        (Transaction.IS_REQUESTER_PRINCIPAL_NO, 'They paid me')
    )

    class Meta:
        model = Transaction
        fields = ['is_requester_principal', 'date', 'amount', 'currency', 'proof_receipt']
        labels = {
            'date': 'What was the date of the transaction?',
            'proof_receipt': 'Screenshot of wire transfer',
            'is_requester_principal': 'Did one of you pay the other?'
        }

    def __init__(self, *args, **kwargs):
        created_by = kwargs.pop('created_by')
        sent_to = kwargs.pop('sent_to')
        super().__init__(*args, **kwargs)

        self.instance.created_by = created_by
        self.instance.sent_to = sent_to

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['amount'].widget.attrs['class'] = 'form-control col-md-4 mr-2'
        self.fields['currency'].widget.attrs['class'] = 'form-control col-md-4 mr-2'
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'

        self.fields['is_requester_principal'].choices = self.IS_REQUESTER_PRINCIPAL_CHOICES


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
        fields = ['submit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        transaction = super().save(commit=False)

        transaction.is_confirmed = self.cleaned_data['submit'] == self.ACTION_CONFIRM

        transaction.save()
        return transaction
