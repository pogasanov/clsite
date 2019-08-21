from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Profile, Transaction


@admin.register(Profile)
class ProfileAdmin(DjangoUserAdmin):
    """Define admin model for custom Profile model with no username field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)


class TransactionVerifiedFilter(admin.SimpleListFilter):

    title = _('Admin Verified')

    parameter_name = 'is_verified'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('Approved')),
            ('no', _('Denied')),
            ('null',  _('Unverified')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(is_verified=True)

        if self.value() == 'no':
            return queryset.filter(is_verified=False)

        if self.value() == 'null':
            return queryset.filter(is_verified__isnull=True)


class TransactionValueInUSDEmptyFilter(admin.SimpleListFilter):

    title = _('Value in USD Empty')

    parameter_name = 'value_in_usd'

    def lookups(self, request, model_admin):

        return (
            ('empty', _('Conversion Pending')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'empty':
            return queryset.filter(value_in_usd__isnull=True)


def mark_as_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)
mark_as_verified.short_description = "Mark selected transactions as verified"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin model for the Transactions."""
    change_list_template = 'transaction_admin.html'
    list_filter = [TransactionVerifiedFilter, TransactionValueInUSDEmptyFilter]
    list_display = (
        'requester', 'amount_direction','requestee', 'amount', 'currency', 'date',
        'value_in_usd', 'currency_conversion', 'is_confirmed', 'is_verified', 'proof_receipt_requester'
    )
    list_editable = ('value_in_usd',)
    ordering = ['-created_at']
    actions = [mark_as_verified]

    class Media:
        css = {'all': ('admin.css',)}

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
