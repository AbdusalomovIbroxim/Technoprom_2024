from django.contrib import admin
from .models import EventLink


@admin.register(EventLink)
class EventLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_datetime', 'end_datetime', 'is_published']
    search_fields = ['title', 'location', 'description']
    list_filter = ['is_published', 'start_datetime', 'end_datetime']
    date_hierarchy = 'start_datetime'
