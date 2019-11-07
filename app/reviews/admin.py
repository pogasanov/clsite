from django.contrib import admin
from .models import Review
from django.utils.html import format_html


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'created_by', 'payment_direction', 'sent_to', 'get_rating',
        'work_description_private', 'recommendation', 'is_deleted'
    )
    search_fields = [
        'created_by__handle', 'created_by__email',
        'sent_to__handle', 'sent_to__email'
    ]
    list_editable = ['is_deleted']
    ordering = ['-created_at']

    class Media:
        css = {'all': ('admin.css',)}

    def payment_direction(self, obj):
        arrow_tag = '<img src="/static/admin/img/tooltag-arrowright.svg" class="{}"alt="None">'

        if obj.is_sender_principal is True:
            return format_html(arrow_tag.format('custom-arrow-right'))
        if obj. is_sender_principal is False:
            return format_html(arrow_tag.format('custom-arrow-left'))
        if obj.is_sender_principal is None:
            return format_html(arrow_tag.format('custom-arrow-left')
                               + '  ' + arrow_tag.format('custom-arrow-right'))

    def get_rating(self, obj):
        return obj.rating
    get_rating.short_description = 'Rating'
