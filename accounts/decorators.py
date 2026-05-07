from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from audit.models import AuditLog
from audit.utils import log_audit


def get_user_role(user):
    profile = getattr(user, "profile", None)

    if not profile:
        return None

    return profile.role


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user

            # Superuser bypass
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Active check
            if not user.is_active:
                messages.error(request, "Your account is inactive.")
                return redirect("login")

            role = get_user_role(user)

            if not role:
                messages.error(request, "Your account profile is not configured.")
                log_audit(
                    request,
                    AuditLog.ACTION_PERMISSION_DENIED,
                    "Accounts",
                    "User has no profile."
                )
                return redirect("dashboard")

            if role not in allowed_roles:
                messages.error(request, "You do not have permission to access that page.")
                log_audit(
                    request,
                    AuditLog.ACTION_PERMISSION_DENIED,
                    "Accounts",
                    f"Blocked access to {request.path}"
                )
                return redirect("dashboard")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator



def super_admin_required(view_func):
    return role_required(["super_admin"])(view_func)


def clerk_or_admin_required(view_func):
    return role_required([
        "super_admin",
        "clerk",
        "deputy_clerk",
    ])(view_func)


def gallery_manager_required(view_func):
    return role_required([
        "super_admin",
        "clerk",
        "deputy_clerk",
        "media_pro",
    ])(view_func)


def legislative_staff_required(view_func):
    return role_required([
        "super_admin",
        "speaker",
        "deputy_speaker",
        "clerk",
        "deputy_clerk",
        "committee_clerk",
        "honourable_member",
        "director_admin_staff",
        "media_pro",
    ])(view_func)