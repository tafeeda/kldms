from django.contrib import admin

from .models import AttendanceRecord, AttendanceSession


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "attendance_type",
        "attendance_date",
        "sitting",
        "committee",
        "is_locked",
        "recorded_by",
    ]
    list_filter = ["attendance_type", "attendance_date", "is_locked"]
    search_fields = ["title", "description", "sitting__title", "committee__name"]
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ["session", "member", "status", "remarks", "recorded_at"]
    list_filter = ["status", "session__attendance_type", "session__attendance_date"]
    search_fields = [
        "member__first_name",
        "member__middle_name",
        "member__last_name",
        "session__title",
        "remarks",
    ]