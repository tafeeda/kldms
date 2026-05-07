from django.conf import settings
from django.db import models

from committees.models import Committee
from members.models import HonourableMember
from sittings.models import PlenarySitting


class AttendanceSession(models.Model):
    TYPE_PLENARY = "plenary"
    TYPE_COMMITTEE = "committee"

    TYPE_CHOICES = [
        (TYPE_PLENARY, "Plenary Sitting"),
        (TYPE_COMMITTEE, "Committee Meeting"),
    ]

    title = models.CharField(max_length=255)
    attendance_type = models.CharField(max_length=30, choices=TYPE_CHOICES)

    sitting = models.ForeignKey(
        PlenarySitting,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attendance_sessions"
    )

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attendance_sessions"
    )

    attendance_date = models.DateField()
    description = models.TextField(blank=True)
    is_locked = models.BooleanField(default=False)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_attendance_sessions"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attendance_date", "-created_at"]

    def __str__(self):
        return self.title

    def present_count(self):
        return self.records.filter(status=AttendanceRecord.STATUS_PRESENT).count()

    def absent_count(self):
        return self.records.filter(status=AttendanceRecord.STATUS_ABSENT).count()

    def late_count(self):
        return self.records.filter(status=AttendanceRecord.STATUS_LATE).count()

    def excused_count(self):
        return self.records.filter(status=AttendanceRecord.STATUS_EXCUSED).count()


class AttendanceRecord(models.Model):
    STATUS_PRESENT = "present"
    STATUS_ABSENT = "absent"
    STATUS_LATE = "late"
    STATUS_EXCUSED = "excused"

    STATUS_CHOICES = [
        (STATUS_PRESENT, "Present"),
        (STATUS_ABSENT, "Absent"),
        (STATUS_LATE, "Late"),
        (STATUS_EXCUSED, "Excused"),
    ]

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )

    member = models.ForeignKey(
        HonourableMember,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    remarks = models.CharField(max_length=255, blank=True)

    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["session", "member"]
        ordering = ["member__last_name", "member__first_name"]

    def __str__(self):
        return f"{self.member} - {self.get_status_display()}"