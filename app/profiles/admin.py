from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Profile, Transaction


@admin.register(Profile)
class ProfileAdmin(DjangoUserAdmin):
    """Define admin model for custom Profile model with no username field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
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
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class IsVerifiedFilter(admin.SimpleListFilter):

    title = _('Is Verified from Admin')

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


def mark_as_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)
mark_as_verified.short_description = "Mark selected transactions as verified"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin model for the Transactions."""
    list_filter = [IsVerifiedFilter]
    list_display = (
        'requester', 'requestee', 'amount', 'currency', 'date', 'is_requester_principal',
        'is_confirmed', 'is_verified', 'proof_receipt_requester'
    )
    ordering = ['-created_at']
    actions = [mark_as_verified]
