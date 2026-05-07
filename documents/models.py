import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_document_file(file):
    allowed_extensions = [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".txt", ".csv", ".jpg",
        ".jpeg", ".png"
    ]

    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(
            "Unsupported file type. Allowed files: PDF, Word, Excel, PowerPoint, TXT, CSV, JPG, PNG."
        )

    blocked_extensions = [
        ".exe", ".bat", ".cmd", ".sh", ".php", ".js",
        ".html", ".htm", ".py", ".zip", ".rar"
    ]

    if ext in blocked_extensions:
        raise ValidationError("This file type is not allowed for security reasons.")

    max_size_mb = 20

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size must not exceed {max_size_mb}MB.")


class DocumentCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Document Categories"

    def __str__(self):
        return self.name


class DocumentFile(models.Model):
    ACCESS_PUBLIC = "public"
    ACCESS_INTERNAL = "internal"
    ACCESS_RESTRICTED = "restricted"

    ACCESS_CHOICES = [
        (ACCESS_PUBLIC, "Public"),
        (ACCESS_INTERNAL, "Internal"),
        (ACCESS_RESTRICTED, "Restricted"),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents"
    )
    description = models.TextField(blank=True)

    file = models.FileField(
        upload_to="central_documents/",
        validators=[validate_document_file]
    )

    access_level = models.CharField(
        max_length=30,
        choices=ACCESS_CHOICES,
        default=ACCESS_INTERNAL
    )

    is_published = models.BooleanField(default=False)
    version_number = models.PositiveIntegerField(default=1)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_documents"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def is_public_document(self):
        return self.access_level == self.ACCESS_PUBLIC and self.is_published

    def __str__(self):
        return self.title


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        DocumentFile,
        on_delete=models.CASCADE,
        related_name="versions"
    )
    version_number = models.PositiveIntegerField()
    file = models.FileField(
        upload_to="central_documents/versions/",
        validators=[validate_document_file]
    )
    notes = models.TextField(blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number", "-uploaded_at"]
        unique_together = ["document", "version_number"]

    def __str__(self):
        return f"{self.document.title} - Version {self.version_number}"


class DocumentAccessLog(models.Model):
    ACTION_VIEW = "view"
    ACTION_DOWNLOAD = "download"

    ACTION_CHOICES = [
        (ACTION_VIEW, "View"),
        (ACTION_DOWNLOAD, "Download"),
    ]

    document = models.ForeignKey(
        DocumentFile,
        on_delete=models.CASCADE,
        related_name="access_logs"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document} - {self.action}"