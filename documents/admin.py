from django.contrib import admin

from .models import (
    DocumentAccessLog,
    DocumentCategory,
    DocumentFile,
    DocumentVersion,
)


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0
    readonly_fields = ["uploaded_at"]


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "access_level",
        "is_published",
        "version_number",
        "uploaded_by",
        "created_at",
    ]
    list_filter = ["access_level", "is_published", "category", "created_at"]
    search_fields = ["title", "description", "category__name"]
    inlines = [DocumentVersionInline]


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ["document", "version_number", "uploaded_by", "uploaded_at"]
    list_filter = ["uploaded_at"]
    search_fields = ["document__title", "notes"]


@admin.register(DocumentAccessLog)
class DocumentAccessLogAdmin(admin.ModelAdmin):
    list_display = ["document", "user", "action", "ip_address", "created_at"]
    list_filter = ["action", "created_at"]
    search_fields = ["document__title", "user__username", "ip_address"]
    readonly_fields = ["document", "user", "action", "ip_address", "user_agent", "created_at"]

    def has_add_permission(self, request):
        return False