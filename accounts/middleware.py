from django.contrib import messages

from audit.models import AuditLog
from audit.utils import get_client_ip, get_device_fingerprint, log_audit


class SuspiciousLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_ip = get_client_ip(request)
            current_fingerprint = get_device_fingerprint(request)

            last_login_log = AuditLog.objects.filter(
                actor=request.user,
                action=AuditLog.ACTION_LOGIN
            ).exclude(
                device_fingerprint=""
            ).order_by("-created_at").first()

            if last_login_log:
                different_ip = last_login_log.ip_address and last_login_log.ip_address != current_ip
                different_device = (
                    last_login_log.device_fingerprint
                    and last_login_log.device_fingerprint != current_fingerprint
                )

                if different_ip or different_device:
                    already_logged = AuditLog.objects.filter(
                        actor=request.user,
                        action=AuditLog.ACTION_SUSPICIOUS,
                        ip_address=current_ip,
                        device_fingerprint=current_fingerprint,
                    ).exists()

                    if not already_logged:
                        log_audit(
                            request,
                            AuditLog.ACTION_SUSPICIOUS,
                            "Security",
                            "Suspicious login/device change detected."
                        )

                        messages.warning(
                            request,
                            "Security notice: this login appears to be from a new device or network."
                        )

        return self.get_response(request)