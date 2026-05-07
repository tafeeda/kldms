import hashlib


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def get_device_fingerprint(request):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    ip_address = get_client_ip(request) or ""

    raw_fingerprint = f"{ip_address}|{user_agent}|{accept_language}"

    return hashlib.sha256(raw_fingerprint.encode("utf-8")).hexdigest()


def log_audit(request, action, module, description, content_object=None):
    from .models import AuditLog

    AuditLog.objects.create(
        actor=request.user if request.user.is_authenticated else None,
        action=action,
        module=module,
        description=description,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        device_fingerprint=get_device_fingerprint(request),
    )