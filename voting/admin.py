from django.contrib import admin

from .models import VoteRecord, VoteSession


class VoteRecordInline(admin.TabularInline):
    model = VoteRecord
    extra = 0


@admin.register(VoteSession)
class VoteSessionAdmin(admin.ModelAdmin):
    list_display = [
        "vote_number",
        "title",
        "vote_type",
        "vote_method",
        "outcome",
        "vote_date",
        "is_open",
        "is_locked",
        "is_public",
    ]
    list_filter = [
        "vote_type",
        "vote_method",
        "outcome",
        "vote_date",
        "is_open",
        "is_locked",
        "is_public",
    ]
    search_fields = [
        "vote_number",
        "title",
        "description",
        "decision_summary",
        "bill__title",
        "motion__title",
        "resolution__title",
        "sitting__title",
    ]
    inlines = [VoteRecordInline]


@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ["session", "member", "choice", "remarks", "voted_at"]
    list_filter = ["choice", "session__vote_type", "session__vote_date"]
    search_fields = [
        "session__title",
        "session__vote_number",
        "member__first_name",
        "member__last_name",
        "remarks",
    ]