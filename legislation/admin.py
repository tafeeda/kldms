from django.contrib import admin
from .models import (
    Bill,
    BillAmendment,
    BillDocument,
    BillReading,
    Motion,
    MotionDocument,
    Resolution,
    ResolutionDocument,
)



class BillReadingInline(admin.TabularInline):
    model = BillReading
    extra = 0


class BillAmendmentInline(admin.TabularInline):
    model = BillAmendment
    extra = 0


class BillDocumentInline(admin.TabularInline):
    model = BillDocument
    extra = 0


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = [
        "bill_number",
        "title",
        "sponsor",
        "status",
        "is_public",
        "is_archived",
        "created_at",
    ]
    list_filter = ["status", "is_public", "is_archived", "created_at"]
    search_fields = [
        "title",
        "bill_number",
        "summary",
        "long_title",
        "sponsor__first_name",
        "sponsor__last_name",
    ]
    filter_horizontal = ["co_sponsors"]
    inlines = [BillReadingInline, BillAmendmentInline, BillDocumentInline]


@admin.register(BillReading)
class BillReadingAdmin(admin.ModelAdmin):
    list_display = ["bill", "reading_type", "reading_date", "recorded_by"]
    list_filter = ["reading_type", "reading_date"]
    search_fields = ["bill__title", "bill__bill_number", "notes"]


@admin.register(BillAmendment)
class BillAmendmentAdmin(admin.ModelAdmin):
    list_display = ["title", "bill", "proposed_by", "amendment_date", "is_approved"]
    list_filter = ["is_approved", "amendment_date"]
    search_fields = ["title", "description", "bill__title"]


@admin.register(BillDocument)
class BillDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "bill", "is_public", "uploaded_by", "uploaded_at"]
    list_filter = ["is_public", "uploaded_at"]
    search_fields = ["title", "description", "bill__title", "bill__bill_number"]



class MotionDocumentInline(admin.TabularInline):
    model = MotionDocument
    extra = 0


@admin.register(Motion)
class MotionAdmin(admin.ModelAdmin):
    list_display = [
        "motion_number",
        "title",
        "sponsor",
        "status",
        "is_public",
        "is_archived",
        "created_at",
    ]
    list_filter = ["status", "is_public", "is_archived", "created_at"]
    search_fields = [
        "title",
        "motion_number",
        "description",
        "decision",
        "sponsor__first_name",
        "sponsor__last_name",
    ]
    filter_horizontal = ["co_sponsors"]
    inlines = [MotionDocumentInline]


@admin.register(MotionDocument)
class MotionDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "motion", "is_public", "uploaded_by", "uploaded_at"]
    list_filter = ["is_public", "uploaded_at"]
    search_fields = ["title", "description", "motion__title", "motion__motion_number"]


class ResolutionDocumentInline(admin.TabularInline):
    model = ResolutionDocument
    extra = 0


@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    list_display = [
        "resolution_number",
        "title",
        "related_motion",
        "status",
        "is_public",
        "date_adopted",
        "created_at",
    ]
    list_filter = ["status", "is_public", "date_adopted", "created_at"]
    search_fields = [
        "title",
        "resolution_number",
        "description",
        "decision_summary",
        "related_motion__title",
        "related_motion__motion_number",
    ]
    inlines = [ResolutionDocumentInline]


@admin.register(ResolutionDocument)
class ResolutionDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "resolution", "is_public", "uploaded_by", "uploaded_at"]
    list_filter = ["is_public", "uploaded_at"]
    search_fields = [
        "title",
        "description",
        "resolution__title",
        "resolution__resolution_number",
    ]