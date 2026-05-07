from django.conf import settings
from django.db import models

from legislation.models import Bill, Motion, Resolution
from members.models import HonourableMember
from sittings.models import PlenarySitting


class VoteSession(models.Model):
    TYPE_BILL = "bill"
    TYPE_MOTION = "motion"
    TYPE_RESOLUTION = "resolution"
    TYPE_OTHER = "other"

    TYPE_CHOICES = [
        (TYPE_BILL, "Bill"),
        (TYPE_MOTION, "Motion"),
        (TYPE_RESOLUTION, "Resolution"),
        (TYPE_OTHER, "Other Matter"),
    ]

    METHOD_ELECTRONIC = "electronic"
    METHOD_VOICE = "voice"
    METHOD_DIVISION = "division"

    METHOD_CHOICES = [
        (METHOD_ELECTRONIC, "Electronic Vote"),
        (METHOD_VOICE, "Voice Vote"),
        (METHOD_DIVISION, "Division Vote"),
    ]

    OUTCOME_PENDING = "pending"
    OUTCOME_CARRIED = "carried"
    OUTCOME_NEGATIVED = "negatived"
    OUTCOME_TIED = "tied"

    OUTCOME_CHOICES = [
        (OUTCOME_PENDING, "Pending"),
        (OUTCOME_CARRIED, "Carried"),
        (OUTCOME_NEGATIVED, "Negatived"),
        (OUTCOME_TIED, "Tied"),
    ]

    title = models.CharField(max_length=255)
    vote_number = models.CharField(max_length=100, unique=True)

    vote_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    vote_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default=METHOD_ELECTRONIC)

    sitting = models.ForeignKey(
        PlenarySitting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vote_sessions"
    )

    bill = models.ForeignKey(
        Bill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vote_sessions"
    )

    motion = models.ForeignKey(
        Motion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vote_sessions"
    )

    resolution = models.ForeignKey(
        Resolution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vote_sessions"
    )

    description = models.TextField(blank=True)
    outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, default=OUTCOME_PENDING)
    decision_summary = models.TextField(blank=True)

    vote_date = models.DateField()
    is_open = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_vote_sessions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-vote_date", "-created_at"]

    def __str__(self):
        return f"{self.vote_number} - {self.title}"

    def yes_count(self):
        return self.records.filter(choice=VoteRecord.CHOICE_YES).count()

    def no_count(self):
        return self.records.filter(choice=VoteRecord.CHOICE_NO).count()

    def abstain_count(self):
        return self.records.filter(choice=VoteRecord.CHOICE_ABSTAIN).count()

    def total_votes(self):
        return self.records.count()


class VoteRecord(models.Model):
    CHOICE_YES = "yes"
    CHOICE_NO = "no"
    CHOICE_ABSTAIN = "abstain"

    CHOICE_CHOICES = [
        (CHOICE_YES, "Yes"),
        (CHOICE_NO, "No"),
        (CHOICE_ABSTAIN, "Abstain"),
    ]

    session = models.ForeignKey(
        VoteSession,
        on_delete=models.CASCADE,
        related_name="records"
    )

    member = models.ForeignKey(
        HonourableMember,
        on_delete=models.CASCADE,
        related_name="vote_records"
    )

    choice = models.CharField(max_length=20, choices=CHOICE_CHOICES)
    remarks = models.CharField(max_length=255, blank=True)

    voted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["session", "member"]
        ordering = ["member__last_name", "member__first_name"]

    def __str__(self):
        return f"{self.member} - {self.get_choice_display()}"