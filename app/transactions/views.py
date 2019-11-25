from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TransactionForm, ConfirmTransactionForm
from .models import Transaction


def transaction(request, handle):
    created_by = request.user
    sent_to = get_object_or_404(get_user_model(), handle=handle)

    if created_by == sent_to:
        return redirect('profile')

    form = TransactionForm(request.POST or None,
                           request.FILES or None,
                           created_by=created_by,
                           sent_to=sent_to)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(
            request,
            "Thank you. We have contacted {} to confirm the transaction with the following details.".format(
                sent_to.full_name.upper()),
        )
        return redirect('home')

    return render(request, "transaction.html", context={'form': form})


def confirm_transaction(request, transaction_id):
    user = request.user
    user_transaction = get_object_or_404(Transaction, id=transaction_id)

    if user_transaction not in user.unconfirmed_transactions():
        return redirect('profile')

    form = ConfirmTransactionForm(request.POST or None, instance=user_transaction)

    if request.POST and form.is_valid():
        form.save()
        return redirect('home')

    context = {
        'transaction': user_transaction,
        'form': form
    }

    return render(request, "confirm_transaction.html", context=context)
