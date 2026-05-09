from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from accounts.decorators import super_admin_required
from .models import AuditLog


@super_admin_required
def audit_log_list(request):
    query = request.GET.get("q", "").strip()
    action = request.GET.get("action", "").strip()
    module = request.GET.get("module", "").strip()

    logs = AuditLog.objects.select_related("actor").all().order_by("-created_at")

    if query:
        logs = logs.filter(
            Q(actor__username__icontains=query) |
            Q(actor__first_name__icontains=query) |
            Q(actor__last_name__icontains=query) |
            Q(module__icontains=query) |
            Q(action__icontains=query) |
            Q(description__icontains=query) |
            Q(ip_address__icontains=query) |
            Q(device_fingerprint__icontains=query)
        )

    if action:
        logs = logs.filter(action=action)

    if module:
        logs = logs.filter(module=module)

    modules = AuditLog.objects.exclude(module="").values_list("module", flat=True).distinct().order_by("module")

    return render(request, "audit/audit_log_list.html", {
        "page_title": "Audit Logs",
        "logs": logs[:500],
        "query": query,
        "action": action,
        "module": module,
        "modules": modules,
        "action_choices": AuditLog.ACTION_CHOICES,
    })