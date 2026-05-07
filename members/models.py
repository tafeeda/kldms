from django.conf import settings
from django.db import models

from constituencies.models import Constituency, PoliticalParty


class HonourableMember(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_FORMER = "former"
    STATUS_SUSPENDED = "suspended"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_FORMER, "Former"),
        (STATUS_SUSPENDED, "Suspended"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    user_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="member_profile"
    )

    title = models.CharField(max_length=50, default="Hon.")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    photo = models.ImageField(upload_to="member_photos/", blank=True, null=True)

    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members"
    )

    political_party = models.ForeignKey(
        PoliticalParty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members"
    )

    position_title = models.CharField(
        max_length=150,
        blank=True,
        help_text="Example: Speaker, Deputy Speaker, Majority Leader, Member"
    )

    biography = models.TextField(blank=True)
    date_sworn_in = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_members"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "last_name", "first_name"]

    @property
    def full_name(self):
        names = [self.title, self.first_name, self.middle_name, self.last_name]
        return " ".join([name for name in names if name])

    def __str__(self):
        return self.full_name