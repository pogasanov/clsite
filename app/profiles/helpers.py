from django.db.models import Q

from transactions.models import Transaction


def get_user_relationships(user):
    """
    This method returns users all transactions ordered by user with which the transaction happened
    :param user: user to get all the transactions for
    :return: returns a dictionary that has user handle as key and list of transactions as value
    """
    transactions = {}
    _filter = (Q(requester=user) | Q(requestee=user)) & Q(is_confirmed=True)

    for transaction in  Transaction.objects.filter(_filter):
        other_user_handle = transaction.requester.handle

        if user == transaction.requester:
            other_user_handle = transaction.requestee.handle

        if other_user_handle not in transactions:
            transactions[other_user_handle] = []

        transactions[other_user_handle].append(transaction)

    return transactions
