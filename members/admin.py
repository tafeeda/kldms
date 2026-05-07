from django.contrib import admin

from .models import HonourableMember


@admin.register(HonourableMember)
class HonourableMemberAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "constituency",
        "political_party",
        "position_title",
        "status",
        "is_published",
        "display_order",
    ]
    list_filter = ["status", "is_published", "political_party", "constituency"]
    search_fields = [
        "first_name",
        "middle_name",
        "last_name",
        "position_title",
        "constituency__name",
        "political_party__name",
    ]
    ordering = ["display_order", "last_name"]