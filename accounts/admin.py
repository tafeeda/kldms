from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "role",
        "official_title",
        "phone",
        "is_active_staff",
        "created_at",
    ]
    list_filter = ["role", "is_active_staff", "created_at"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "phone"]
    readonly_fields = ["created_at", "updated_at"]