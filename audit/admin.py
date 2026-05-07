from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = [
        "actor",
        "action",
        "module",
        "ip_address",
        "device_fingerprint",
        "created_at",
    ]
    list_filter = ["action", "module", "created_at"]
    search_fields = [
        "actor__username",
        "action",
        "module",
        "description",
        "ip_address",
        "device_fingerprint",
        "user_agent",
    ]
    readonly_fields = [
        "actor",
        "action",
        "module",
        "description",
        "ip_address",
        "user_agent",
        "device_fingerprint",
        "created_at",
    ]

    def has_add_permission(self, request):
        return False