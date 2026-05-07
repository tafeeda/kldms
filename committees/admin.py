from django.contrib import admin

from .models import Committee, CommitteeDocument, CommitteeMembership


class CommitteeMembershipInline(admin.TabularInline):
    model = CommitteeMembership
    extra = 1


class CommitteeDocumentInline(admin.TabularInline):
    model = CommitteeDocument
    extra = 0
    readonly_fields = ["uploaded_at"]


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "committee_type",
        "chairman",
        "vice_chairman",
        "committee_clerk",
        "is_active",
        "display_order",
    ]
    list_filter = ["committee_type", "is_active", "created_at"]
    search_fields = [
        "name",
        "description",
        "chairman__first_name",
        "chairman__last_name",
        "vice_chairman__first_name",
        "vice_chairman__last_name",
    ]
    inlines = [CommitteeMembershipInline, CommitteeDocumentInline]


@admin.register(CommitteeMembership)
class CommitteeMembershipAdmin(admin.ModelAdmin):
    list_display = ["committee", "member", "role", "date_joined", "is_active"]
    list_filter = ["role", "is_active", "committee"]
    search_fields = ["committee__name", "member__first_name", "member__last_name"]


@admin.register(CommitteeDocument)
class CommitteeDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "committee",
        "access_level",
        "is_published",
        "uploaded_by",
        "uploaded_at",
    ]
    list_filter = ["access_level", "is_published", "uploaded_at", "committee"]
    search_fields = ["title", "description", "committee__name"]