from django.conf import settings
from django.db import models

from members.models import HonourableMember


class Committee(models.Model):
    TYPE_STANDING = "standing"
    TYPE_SPECIAL = "special"
    TYPE_ADHOC = "adhoc"

    TYPE_CHOICES = [
        (TYPE_STANDING, "Standing Committee"),
        (TYPE_SPECIAL, "Special Committee"),
        (TYPE_ADHOC, "Ad-hoc Committee"),
    ]

    name = models.CharField(max_length=200, unique=True)
    committee_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=TYPE_STANDING)
    description = models.TextField(blank=True)

    chairman = models.ForeignKey(
        HonourableMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chaired_committees"
    )

    vice_chairman = models.ForeignKey(
        HonourableMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vice_chaired_committees"
    )

    committee_clerk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_committees"
    )

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_committees"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class CommitteeMembership(models.Model):
    ROLE_MEMBER = "member"
    ROLE_SECRETARY = "secretary"
    ROLE_OBSERVER = "observer"

    ROLE_CHOICES = [
        (ROLE_MEMBER, "Member"),
        (ROLE_SECRETARY, "Secretary"),
        (ROLE_OBSERVER, "Observer"),
    ]

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    member = models.ForeignKey(
        HonourableMember,
        on_delete=models.CASCADE,
        related_name="committee_memberships"
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    date_joined = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["committee", "member"]
        ordering = ["member__last_name", "member__first_name"]

    def __str__(self):
        return f"{self.member} - {self.committee}"


class CommitteeDocument(models.Model):
    ACCESS_INTERNAL = "internal"
    ACCESS_PUBLIC = "public"
    ACCESS_RESTRICTED = "restricted"

    ACCESS_CHOICES = [
        (ACCESS_INTERNAL, "Internal"),
        (ACCESS_PUBLIC, "Public"),
        (ACCESS_RESTRICTED, "Restricted"),
    ]

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="committee_documents/")
    access_level = models.CharField(max_length=30, choices=ACCESS_CHOICES, default=ACCESS_INTERNAL)
    is_published = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_committee_documents"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title