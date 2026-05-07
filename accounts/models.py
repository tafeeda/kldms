from django.conf import settings
from django.db import models
from django.utils import timezone




class FailedLoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    attempt_count = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.attempt_count} attempts"


class UserProfile(models.Model):
    ROLE_SUPER_ADMIN = "super_admin"
    ROLE_SPEAKER = "speaker"
    ROLE_DEPUTY_SPEAKER = "deputy_speaker"
    ROLE_CLERK = "clerk"
    ROLE_DEPUTY_CLERK = "deputy_clerk"
    ROLE_COMMITTEE_CLERK = "committee_clerk"
    ROLE_MEMBER = "honourable_member"
    ROLE_DIRECTOR = "director_admin_staff"
    ROLE_MEDIA = "media_pro"

    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, "Super Admin"),
        (ROLE_SPEAKER, "Speaker"),
        (ROLE_DEPUTY_SPEAKER, "Deputy Speaker"),
        (ROLE_CLERK, "Clerk of the House"),
        (ROLE_DEPUTY_CLERK, "Deputy Clerk"),
        (ROLE_COMMITTEE_CLERK, "Committee Clerk"),
        (ROLE_MEMBER, "Honourable Member"),
        (ROLE_DIRECTOR, "Director/Admin Staff"),
        (ROLE_MEDIA, "Media/Public Relations Officer"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    phone = models.CharField(max_length=30, blank=True)
    official_title = models.CharField(max_length=150, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    is_active_staff = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def role_display(self):
        return self.get_role_display()

    def is_super_admin(self):
        return self.role == self.ROLE_SUPER_ADMIN

    def is_speaker(self):
        return self.role == self.ROLE_SPEAKER

    def is_deputy_speaker(self):
        return self.role == self.ROLE_DEPUTY_SPEAKER

    def is_clerk(self):
        return self.role == self.ROLE_CLERK

    def is_deputy_clerk(self):
        return self.role == self.ROLE_DEPUTY_CLERK

    def is_committee_clerk(self):
        return self.role == self.ROLE_COMMITTEE_CLERK

    def is_member(self):
        return self.role == self.ROLE_MEMBER

    def is_director(self):
        return self.role == self.ROLE_DIRECTOR

    def is_media(self):
        return self.role == self.ROLE_MEDIA

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"