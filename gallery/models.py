from django.conf import settings
from django.db import models

from constituencies.models import Constituency, PoliticalParty


class OfficialProfile(models.Model):
    CATEGORY_GOVERNOR = "governor"
    CATEGORY_DEPUTY_GOVERNOR = "deputy_governor"
    CATEGORY_SPEAKER = "speaker"
    CATEGORY_DEPUTY_SPEAKER = "deputy_speaker"
    CATEGORY_CLERK = "clerk"
    CATEGORY_DEPUTY_CLERK = "deputy_clerk"
    CATEGORY_MAJORITY_LEADER = "majority_leader"
    CATEGORY_MINORITY_LEADER = "minority_leader"
    CATEGORY_PRINCIPAL_OFFICER = "principal_officer"
    CATEGORY_HON_MEMBER = "honourable_member"
    CATEGORY_GOVT_OFFICIAL = "government_official"
    CATEGORY_FORMER_OFFICIAL = "former_official"

    CATEGORY_CHOICES = [
        (CATEGORY_GOVERNOR, "Governor"),
        (CATEGORY_DEPUTY_GOVERNOR, "Deputy Governor"),
        (CATEGORY_SPEAKER, "Speaker"),
        (CATEGORY_DEPUTY_SPEAKER, "Deputy Speaker"),
        (CATEGORY_CLERK, "Clerk of the House"),
        (CATEGORY_DEPUTY_CLERK, "Deputy Clerk"),
        (CATEGORY_MAJORITY_LEADER, "Majority Leader"),
        (CATEGORY_MINORITY_LEADER, "Minority Leader"),
        (CATEGORY_PRINCIPAL_OFFICER, "Principal Officer"),
        (CATEGORY_HON_MEMBER, "Honourable Member"),
        (CATEGORY_GOVT_OFFICIAL, "Government Official"),
        (CATEGORY_FORMER_OFFICIAL, "Former Official"),
    ]

    STATUS_CURRENT = "current"
    STATUS_FORMER = "former"

    STATUS_CHOICES = [
        (STATUS_CURRENT, "Current"),
        (STATUS_FORMER, "Former"),
    ]

    full_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    photo = models.ImageField(upload_to="official_photos/", blank=True, null=True)

    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="official_profiles"
    )

    political_party = models.ForeignKey(
        PoliticalParty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="official_profiles"
    )

    short_biography = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CURRENT)

    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_official_profiles"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "category", "full_name"]

    def __str__(self):
        return f"{self.full_name} - {self.position_title}"