from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from attendance.models import AttendanceRecord, AttendanceSession
from committees.models import Committee
from documents.models import DocumentFile
from gallery.models import OfficialProfile
from legislation.models import Bill, Motion, Resolution
from members.models import HonourableMember
from sittings.models import PlenarySitting
from voting.models import VoteRecord, VoteSession


@login_required
def reports_dashboard(request):
    bill_status_data = list(
        Bill.objects.values("status").annotate(total=Count("id")).order_by("status")
    )

    motion_status_data = list(
        Motion.objects.values("status").annotate(total=Count("id")).order_by("status")
    )

    resolution_status_data = list(
        Resolution.objects.values("status").annotate(total=Count("id")).order_by("status")
    )

    attendance_status_data = list(
        AttendanceRecord.objects.values("status").annotate(total=Count("id")).order_by("status")
    )

    vote_choice_data = list(
        VoteRecord.objects.values("choice").annotate(total=Count("id")).order_by("choice")
    )

    document_access_data = list(
        DocumentFile.objects.values("access_level").annotate(total=Count("id")).order_by("access_level")
    )

    context = {
        "page_title": "Reports & Analytics",

        "total_members": HonourableMember.objects.count(),
        "active_members": HonourableMember.objects.filter(status="active").count(),
        "total_committees": Committee.objects.count(),
        "total_bills": Bill.objects.count(),
        "public_bills": Bill.objects.filter(is_public=True).count(),
        "passed_bills": Bill.objects.filter(status="passed").count(),
        "total_motions": Motion.objects.count(),
        "adopted_motions": Motion.objects.filter(status="adopted").count(),
        "total_resolutions": Resolution.objects.count(),
        "public_resolutions": Resolution.objects.filter(is_public=True).count(),
        "total_sittings": PlenarySitting.objects.count(),
        "completed_sittings": PlenarySitting.objects.filter(status="completed").count(),
        "total_attendance_sessions": AttendanceSession.objects.count(),
        "total_vote_sessions": VoteSession.objects.count(),
        "carried_votes": VoteSession.objects.filter(outcome="carried").count(),
        "total_documents": DocumentFile.objects.count(),
        "public_documents": DocumentFile.objects.filter(access_level="public", is_published=True).count(),
        "published_officials": OfficialProfile.objects.filter(is_published=True).count(),

        "bill_status_labels": [item["status"].replace("_", " ").title() for item in bill_status_data],
        "bill_status_values": [item["total"] for item in bill_status_data],

        "motion_status_labels": [item["status"].replace("_", " ").title() for item in motion_status_data],
        "motion_status_values": [item["total"] for item in motion_status_data],

        "resolution_status_labels": [item["status"].replace("_", " ").title() for item in resolution_status_data],
        "resolution_status_values": [item["total"] for item in resolution_status_data],

        "attendance_status_labels": [item["status"].replace("_", " ").title() for item in attendance_status_data],
        "attendance_status_values": [item["total"] for item in attendance_status_data],

        "vote_choice_labels": [item["choice"].replace("_", " ").title() for item in vote_choice_data],
        "vote_choice_values": [item["total"] for item in vote_choice_data],

        "document_access_labels": [item["access_level"].replace("_", " ").title() for item in document_access_data],
        "document_access_values": [item["total"] for item in document_access_data],
    }

    return render(request, "reports/reports_dashboard.html", context)


@login_required
def printable_report(request):
    context = {
        "page_title": "Printable KLDMS Report",
        "total_members": HonourableMember.objects.count(),
        "active_members": HonourableMember.objects.filter(status="active").count(),
        "total_committees": Committee.objects.count(),
        "total_bills": Bill.objects.count(),
        "public_bills": Bill.objects.filter(is_public=True).count(),
        "passed_bills": Bill.objects.filter(status="passed").count(),
        "total_motions": Motion.objects.count(),
        "adopted_motions": Motion.objects.filter(status="adopted").count(),
        "total_resolutions": Resolution.objects.count(),
        "total_sittings": PlenarySitting.objects.count(),
        "total_attendance_sessions": AttendanceSession.objects.count(),
        "total_vote_sessions": VoteSession.objects.count(),
        "total_documents": DocumentFile.objects.count(),
        "published_officials": OfficialProfile.objects.filter(is_published=True).count(),
    }

    return render(request, "reports/printable_report.html", context)