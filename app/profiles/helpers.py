from django.db.models import Q

from transactions.models import Transaction


def get_user_relationships(user):
    """
    This method returns users all transactions ordered by user with which the transaction happened
    :param user: user to get all the transactions for
    :return: returns a dictionary that has user handle as key and list of transactions as value
    """
    transactions = {}

    for transaction in Transaction.ready.filter(Q(created_by=user) | Q(sent_to=user)):
        other_user_handle = transaction.created_by.handle

        if user == transaction.created_by:
            other_user_handle = transaction.sent_to.handle

        if other_user_handle not in transactions:
            transactions[other_user_handle] = []

        transactions[other_user_handle].append(transaction)

    return transactions
