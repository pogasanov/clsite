from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TransactionForm, ConfirmTransactionForm
from .models import Transaction


@login_required
def transaction(request, handle):
    user = request.user
    receiver = get_object_or_404(get_user_model(), handle=handle)

    if user == receiver:
        return HttpResponseBadRequest()

    transaction_form = TransactionForm(request.POST or None, request.FILES or None)

    if transaction_form.is_valid():
        if transaction_form.files:
            transaction_form.save(requester=user, requestee=receiver, is_proof_by_requester=True)
        else:
            transaction_form.save(requester=user, requestee=receiver)
        messages.info(
            request,
            "Thank you. We have contacted {} to confirm the transaction with the following details.".format(
                receiver.full_name.upper()),
        )
        return redirect('home')

    return render(request, "transaction.html", context={'form': transaction_form})


@login_required
def confirm_transaction(request, transaction_id):
    user = request.user
    user_transaction = get_object_or_404(Transaction, id=transaction_id)

    if user_transaction != user.user_unconfirmed_transaction():
        return HttpResponseBadRequest()

    form = ConfirmTransactionForm(request.POST or None, initial={'requestee_review': 'N'}, instance=user_transaction)

    if request.POST and form.is_valid():
        is_confirmed = request.POST['submit'] != 'deny'
        form.save(is_confirmed=is_confirmed)

        return redirect('home')

    context = {
        'transaction': user_transaction,
        'form': form
    }

    return render(request, "confirm_transaction.html", context=context)
