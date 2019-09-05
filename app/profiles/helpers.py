from django.db.models import Q

from transactions.models import Transaction


def get_user_relationships(user):
    """
    This method returns users all transactions ordered by user with which the transaction happened
    :param user: user to get all the transactions for
    :return: returns a dictionary that has user handle as key and list of transactions as value
    """
    transactions = {}
    all_user_transaction = Transaction.objects.filter(Q(requester=user) | Q(requestee=user))
    ready_user_transaction = [transaction for transaction in all_user_transaction if transaction.is_ready]
    for transaction in ready_user_transaction:
        other_user_handle = transaction.requester.handle

        if user == transaction.requester:
            other_user_handle = transaction.requestee.handle

        if other_user_handle not in transactions:
            transactions[other_user_handle] = []

        transactions[other_user_handle].append(transaction)

    return transactions
