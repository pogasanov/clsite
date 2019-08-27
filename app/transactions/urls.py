from django.urls import path

from . import views

urlpatterns = [
    path('transaction/<handle>', views.transaction, name='create_transaction'),
    path('confirm-transaction/<transaction_id>', views.confirm_transaction, name='confirm_transaction')
]
