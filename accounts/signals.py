from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, FailedLoginAttempt
from audit.utils import get_client_ip

User = get_user_model()

MAX_ATTEMPTS = 5
LOCK_DURATION = 10  # minutes


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        role = UserProfile.ROLE_SUPER_ADMIN if instance.is_superuser else UserProfile.ROLE_MEMBER
        UserProfile.objects.create(user=instance, role=role)
    else:
        UserProfile.objects.get_or_create(user=instance)
        instance.profile.save()


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username")
    ip = get_client_ip(request)

    record, created = FailedLoginAttempt.objects.get_or_create(
        username=username,
        ip_address=ip,
    )

    if record.is_locked:
        return

    record.attempt_count += 1

    if record.attempt_count >= MAX_ATTEMPTS:
        record.is_locked = True
        record.locked_until = timezone.now() + timedelta(minutes=LOCK_DURATION)

    record.save()


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    ip = get_client_ip(request)

    FailedLoginAttempt.objects.filter(
        username=user.username,
        ip_address=ip
    ).delete()