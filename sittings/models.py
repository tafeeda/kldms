from django.conf import settings
from django.db import models


class PlenarySitting(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_ADJOURNED = "adjourned"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_ADJOURNED, "Adjourned"),
    ]

    title = models.CharField(max_length=255)
    sitting_number = models.CharField(max_length=100, unique=True)
    sitting_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, default="Kano State House of Assembly Chamber")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    description = models.TextField(blank=True)

    is_public = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_sittings"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-sitting_date", "-created_at"]

    def __str__(self):
        return f"{self.sitting_number} - {self.title}"


class SittingAgendaItem(models.Model):
    sitting = models.ForeignKey(
        PlenarySitting,
        on_delete=models.CASCADE,
        related_name="agenda_items"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order_number = models.PositiveIntegerField(default=1)
    presenter = models.CharField(max_length=255, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["order_number", "id"]

    def __str__(self):
        return self.title


class OrderPaper(models.Model):
    sitting = models.OneToOneField(
        PlenarySitting,
        on_delete=models.CASCADE,
        related_name="order_paper"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="order_papers/", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prepared_order_papers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VotesProceeding(models.Model):
    sitting = models.OneToOneField(
        PlenarySitting,
        on_delete=models.CASCADE,
        related_name="votes_proceeding"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="votes_proceedings/", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prepared_votes_proceedings"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class HansardTranscript(models.Model):
    sitting = models.OneToOneField(
        PlenarySitting,
        on_delete=models.CASCADE,
        related_name="hansard"
    )
    title = models.CharField(max_length=255)
    transcript = models.TextField()
    file = models.FileField(upload_to="hansards/", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prepared_hansards"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SittingDocument(models.Model):
    sitting = models.ForeignKey(
        PlenarySitting,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="sitting_documents/")
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