from django.contrib import admin

from .models import User, Complaint


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'is_business_account', ]


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ["complaint_type", "sender", "recipient", "created_at"]
    search_fields = ["complaint_type", "sender__username", "recipient__username"]
