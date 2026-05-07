from django.contrib import admin

from .models import (
    HansardTranscript,
    OrderPaper,
    PlenarySitting,
    SittingAgendaItem,
    SittingDocument,
    VotesProceeding,
)


class SittingAgendaItemInline(admin.TabularInline):
    model = SittingAgendaItem
    extra = 1


class SittingDocumentInline(admin.TabularInline):
    model = SittingDocument
    extra = 0


@admin.register(PlenarySitting)
class PlenarySittingAdmin(admin.ModelAdmin):
    list_display = [
        "sitting_number",
        "title",
        "sitting_date",
        "status",
        "is_public",
        "created_by",
    ]
    list_filter = ["status", "is_public", "sitting_date", "created_at"]
    search_fields = ["title", "sitting_number", "venue", "description"]
    inlines = [SittingAgendaItemInline, SittingDocumentInline]


@admin.register(SittingAgendaItem)
class SittingAgendaItemAdmin(admin.ModelAdmin):
    list_display = ["sitting", "order_number", "title", "presenter", "is_completed"]
    list_filter = ["is_completed", "sitting"]
    search_fields = ["title", "description", "presenter", "sitting__title"]


@admin.register(OrderPaper)
class OrderPaperAdmin(admin.ModelAdmin):
    list_display = ["title", "sitting", "is_published", "prepared_by", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content", "sitting__title", "sitting__sitting_number"]


@admin.register(VotesProceeding)
class VotesProceedingAdmin(admin.ModelAdmin):
    list_display = ["title", "sitting", "is_published", "prepared_by", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content", "sitting__title", "sitting__sitting_number"]


@admin.register(HansardTranscript)
class HansardTranscriptAdmin(admin.ModelAdmin):
    list_display = ["title", "sitting", "is_published", "prepared_by", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "transcript", "sitting__title", "sitting__sitting_number"]


@admin.register(SittingDocument)
class SittingDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "sitting", "is_public", "uploaded_by", "uploaded_at"]
    list_filter = ["is_public", "uploaded_at"]
    search_fields = ["title", "description", "sitting__title", "sitting__sitting_number"]