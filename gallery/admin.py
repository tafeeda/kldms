from django.contrib import admin

from .models import OfficialProfile


@admin.register(OfficialProfile)
class OfficialProfileAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "position_title",
        "category",
        "constituency",
        "political_party",
        "status",
        "is_published",
        "display_order",
    ]
    list_filter = [
        "category",
        "status",
        "is_published",
        "political_party",
        "constituency",
    ]
    search_fields = [
        "full_name",
        "position_title",
        "short_biography",
        "constituency__name",
        "political_party__name",
        "political_party__abbreviation",
    ]
    ordering = ["display_order", "category", "full_name"]