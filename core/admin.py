from django.contrib import admin

from .models import SystemSetting


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = [
        "institution_name",
        "system_name",
        "short_name",
        "email",
        "phone",
        "updated_at",
    ]

    def has_add_permission(self, request):
        return not SystemSetting.objects.exists()