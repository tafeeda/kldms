from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import UserProfile
from audit.models import AuditLog
from constituencies.models import Constituency, PoliticalParty
from members.models import HonourableMember
from committees.models import Committee
from legislation.models import Bill, Motion, Resolution
from sittings.models import PlenarySitting
from attendance.models import AttendanceRecord, AttendanceSession
from voting.models import VoteRecord, VoteSession
from documents.models import DocumentFile
from gallery.models import OfficialProfile
from django.contrib import messages
from accounts.decorators import super_admin_required
from audit.utils import log_audit
from .forms import SystemSettingForm
from .models import SystemSetting



@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    recent_logs = AuditLog.objects.select_related("actor")[:8]

    context = {
        "page_title": "KLDMS Dashboard",
        "profile": profile,
        "total_members": HonourableMember.objects.count(),
        "active_members": HonourableMember.objects.filter(status="active").count(),
        "total_constituencies": Constituency.objects.count(),
        "total_parties": PoliticalParty.objects.count(),
        "total_committees": Committee.objects.count(),
        "active_committees": Committee.objects.filter(is_active=True).count(),
        "active_bills": Bill.objects.exclude(status__in=["passed", "assented", "rejected", "withdrawn"]).count(),
        "public_bills": Bill.objects.filter(is_public=True).count(),
        "passed_bills": Bill.objects.filter(status="passed").count(),
        "total_motions": Motion.objects.count(),
        "pending_motions": Motion.objects.filter(status__in=["draft", "submitted", "debated"]).count(),
        "adopted_motions": Motion.objects.filter(status="adopted").count(),
        "total_resolutions": Resolution.objects.count(),
        "public_resolutions": Resolution.objects.filter(is_public=True).count(),
        "total_sittings": PlenarySitting.objects.count(),
        "upcoming_sittings": PlenarySitting.objects.filter(status="scheduled").count(),
        "completed_sittings": PlenarySitting.objects.filter(status="completed").count(),
        "total_attendance_sessions": AttendanceSession.objects.count(),
        "present_records": AttendanceRecord.objects.filter(status="present").count(),
        "absent_records": AttendanceRecord.objects.filter(status="absent").count(),
        "total_vote_sessions": VoteSession.objects.count(),
        "carried_votes": VoteSession.objects.filter(outcome="carried").count(),
        "pending_votes": VoteSession.objects.filter(outcome="pending").count(),
        "total_vote_records": VoteRecord.objects.count(),
        "total_documents": DocumentFile.objects.count(),
        "public_documents": DocumentFile.objects.filter(access_level="public", is_published=True).count(),
        "restricted_documents": DocumentFile.objects.filter(access_level="restricted").count(),
        "total_officials": OfficialProfile.objects.count(),
        "published_officials": OfficialProfile.objects.filter(is_published=True).count(),
        "current_officials": OfficialProfile.objects.filter(status="current").count(),
        "active_bills": 0,
        "pending_motions": 0,
        "published_officials": 0,
        "recent_logs": recent_logs,
    }

    return render(request, "core/dashboard.html", context)



@super_admin_required
def system_settings_view(request):
    setting = SystemSetting.get_settings()

    if request.method == "POST":
        form = SystemSettingForm(request.POST, request.FILES, instance=setting)

        if form.is_valid():
            setting = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "System Settings",
                "Updated system branding and configuration.",
                setting
            )

            messages.success(request, "System settings updated successfully.")
            return redirect("system_settings")
    else:
        form = SystemSettingForm(instance=setting)

    return render(request, "core/system_settings.html", {
        "page_title": "System Settings",
        "form": form,
        "setting": setting,
    })