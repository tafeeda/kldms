from django.conf import settings
from django.db import models

from members.models import HonourableMember


class Bill(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_SUBMITTED = "submitted"
    STATUS_FIRST_READING = "first_reading"
    STATUS_SECOND_READING = "second_reading"
    STATUS_COMMITTEE = "committee"
    STATUS_THIRD_READING = "third_reading"
    STATUS_PASSED = "passed"
    STATUS_ASSENTED = "assented"
    STATUS_REJECTED = "rejected"
    STATUS_WITHDRAWN = "withdrawn"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_FIRST_READING, "First Reading"),
        (STATUS_SECOND_READING, "Second Reading"),
        (STATUS_COMMITTEE, "Committee Stage"),
        (STATUS_THIRD_READING, "Third Reading"),
        (STATUS_PASSED, "Passed"),
        (STATUS_ASSENTED, "Assented"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    title = models.CharField(max_length=255)
    bill_number = models.CharField(max_length=100, unique=True)
    summary = models.TextField(blank=True)
    long_title = models.TextField(blank=True)

    sponsor = models.ForeignKey(
        HonourableMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsored_bills"
    )

    co_sponsors = models.ManyToManyField(
        HonourableMember,
        blank=True,
        related_name="co_sponsored_bills"
    )

    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    date_introduced = models.DateField(blank=True, null=True)
    date_passed = models.DateField(blank=True, null=True)
    date_assented = models.DateField(blank=True, null=True)

    is_public = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_bills"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.bill_number} - {self.title}"


class BillReading(models.Model):
    READING_FIRST = "first"
    READING_SECOND = "second"
    READING_THIRD = "third"

    READING_CHOICES = [
        (READING_FIRST, "First Reading"),
        (READING_SECOND, "Second Reading"),
        (READING_THIRD, "Third Reading"),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="readings")
    reading_type = models.CharField(max_length=20, choices=READING_CHOICES)
    reading_date = models.DateField()
    notes = models.TextField(blank=True)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["reading_date"]

    def __str__(self):
        return f"{self.bill} - {self.get_reading_type_display()}"


class BillAmendment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="amendments")
    title = models.CharField(max_length=255)
    description = models.TextField()
    proposed_by = models.ForeignKey(
        HonourableMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposed_amendments"
    )
    amendment_date = models.DateField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class BillDocument(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="bill_documents/")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class Motion(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_SUBMITTED = "submitted"
    STATUS_DEBATED = "debated"
    STATUS_ADOPTED = "adopted"
    STATUS_REJECTED = "rejected"
    STATUS_WITHDRAWN = "withdrawn"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_DEBATED, "Debated"),
        (STATUS_ADOPTED, "Adopted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    title = models.CharField(max_length=255)
    motion_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    sponsor = models.ForeignKey(
        HonourableMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsored_motions"
    )
    co_sponsors = models.ManyToManyField(
        HonourableMember,
        blank=True,
        related_name="co_sponsored_motions"
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    decision = models.TextField(blank=True)
    date_moved = models.DateField(blank=True, null=True)
    date_decided = models.DateField(blank=True, null=True)

    is_public = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_motions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.motion_number} - {self.title}"


class Resolution(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_ADOPTED = "adopted"
    STATUS_REJECTED = "rejected"
    STATUS_IMPLEMENTED = "implemented"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_ADOPTED, "Adopted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_IMPLEMENTED, "Implemented"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    title = models.CharField(max_length=255)
    resolution_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    related_motion = models.ForeignKey(
        Motion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolutions"
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    decision_summary = models.TextField(blank=True)
    date_adopted = models.DateField(blank=True, null=True)

    is_public = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_resolutions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.resolution_number} - {self.title}"


class MotionDocument(models.Model):
    motion = models.ForeignKey(Motion, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="motion_documents/")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class ResolutionDocument(models.Model):
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="resolution_documents/")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title