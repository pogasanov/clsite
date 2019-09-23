from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Transaction


class TransactionApprovedFilter(admin.SimpleListFilter):
    title = _('Admin Approved')

    parameter_name = 'is_admin_approved'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('Admin Approved')),
            ('no', _('Admin Denied')),
            ('null', _('Pending Approval')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(is_admin_approved=True)

        if self.value() == 'no':
            return queryset.filter(is_admin_approved=False)

        if self.value() == 'null':
            return queryset.filter(Q(is_admin_approved__isnull=True), ~Q(proof_receipt=''))


class TransactionValueInUSDEmptyFilter(admin.SimpleListFilter):
    title = _('USD Value Needed')

    parameter_name = 'value_in_usd'

    def lookups(self, request, model_admin):
        return (
            ('empty', _('Conversion Pending')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(value_in_usd__isnull=True)


def approve_transactions(modeladmin, request, queryset):
    queryset.exclude(proof_receipt='').update(is_admin_approved=True)


approve_transactions.short_description = "Approve selected transactions"


def deny_transactions(modeladmin, request, queryset):
    queryset.exclude(proof_receipt='').update(is_admin_approved=False)


deny_transactions.short_description = "Deny selected transactions"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin model for the Transactions."""
    change_list_template = 'transaction_admin.html'
    list_filter = [TransactionApprovedFilter, TransactionValueInUSDEmptyFilter]
    list_display = (
        'requester', 'amount_direction', 'requestee', 'amount', 'currency', 'date',
        'value_in_usd', 'currency_conversion', 'is_confirmed', 'is_verified', 'admin_approved', 'is_ready', 'proof_receipt'
    )
    list_editable = ('value_in_usd',)
    ordering = ['-created_at']
    actions = [approve_transactions, deny_transactions]

    class Media:
        css = {'all': ('admin.css',)}

    def is_ready(self, obj):
        return obj.is_ready

    is_ready.boolean = True

    def is_verified(self, obj):
        return obj.is_verified

    is_verified.boolean = True

    def admin_approved(self, obj):
        if not obj.proof_receipt:
            return 'N/A'

        if obj.is_admin_approved is None:
            return 'Pending'

        return 'Approved' if obj.is_admin_approved else 'Denied'

    admin_approved.short_description = 'Admin-Approved'

    def amount_direction(self, obj):
        arrow_tag = '<img src="/static/admin/img/tooltag-arrowright.svg" class="{}"alt="None">'

        if obj.is_requester_principal:
            return format_html(arrow_tag.format('custom-arrow-right'))

        return format_html(arrow_tag.format('custom-arrow-left'))

    amount_direction.allow_tags = True
    amount_direction.short_description = ''

    def currency_conversion(self, obj):
        currency_code = obj.currency

        if currency_code == 'USD':
            return

        if obj.value_in_usd:
            return

        date = str(obj.date)
        base_url_f = 'https://www.xe.com/currencytables/?from={currency_code}&date={date}'
        currency_url_f = '<a href="{url}" target="_blank">{currency_code} to USD</a>'

        url = base_url_f.format(currency_code=currency_code, date=date)

        return format_html(currency_url_f.format(url=url, currency_code=currency_code))

    currency_conversion.allow_tags = True
    currency_conversion.short_description = 'Historical Currency URL'
