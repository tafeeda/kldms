from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from audit.models import AuditLog
from audit.utils import log_audit

from attendance.models import AttendanceSession
from committees.models import Committee
from documents.models import DocumentFile
from gallery.models import OfficialProfile
from legislation.models import Bill, Motion, Resolution
from members.models import HonourableMember
from sittings.models import PlenarySitting
from voting.models import VoteSession


def user_role(user):
    profile = getattr(user, "profile", None)
    return profile.role if profile else None


def can_manage_sensitive(role):
    return role in ["super_admin", "clerk", "deputy_clerk"]


def can_view_internal(role):
    return role in [
        "super_admin",
        "speaker",
        "deputy_speaker",
        "clerk",
        "deputy_clerk",
        "committee_clerk",
        "honourable_member",
        "director_admin_staff",
        "media_pro",
    ]


def add_result(results, item_type, title, description, url, icon):
    results.append({
        "type": item_type,
        "title": title,
        "description": description or "",
        "url": url,
        "icon": icon,
    })


@login_required
def live_master_search(request):
    query = request.GET.get("q", "").strip()
    role = user_role(request.user)

    results = []

    if len(query) < 2:
        return JsonResponse({"results": []})

    if not can_view_internal(role):
        log_audit(
            request,
            AuditLog.ACTION_PERMISSION_DENIED,
            "Master Search",
            "User attempted search without valid role."
        )
        return JsonResponse({"results": []})

    # Honourable Members
    members = HonourableMember.objects.select_related(
        "constituency",
        "political_party"
    ).filter(
        Q(first_name__icontains=query) |
        Q(middle_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(position_title__icontains=query) |
        Q(constituency__name__icontains=query) |
        Q(political_party__name__icontains=query) |
        Q(political_party__abbreviation__icontains=query)
    )[:5]

    for member in members:
        add_result(
            results,
            "Member",
            member.full_name,
            f"{member.position_title or 'Honourable Member'} | {member.constituency or '-'}",
            reverse("member_detail", args=[member.id]),
            "👤"
        )

    # Committees
    committees = Committee.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(chairman__first_name__icontains=query) |
        Q(chairman__last_name__icontains=query)
    )[:5]

    for committee in committees:
        add_result(
            results,
            "Committee",
            committee.name,
            committee.description[:120],
            reverse("committee_detail", args=[committee.id]),
            "🏛️"
        )

    # Bills
    bills = Bill.objects.select_related("sponsor").filter(
        Q(title__icontains=query) |
        Q(bill_number__icontains=query) |
        Q(summary__icontains=query) |
        Q(long_title__icontains=query) |
        Q(sponsor__first_name__icontains=query) |
        Q(sponsor__last_name__icontains=query)
    )[:5]

    for bill in bills:
        add_result(
            results,
            "Bill",
            f"{bill.bill_number} - {bill.title}",
            f"Status: {bill.get_status_display()} | Sponsor: {bill.sponsor or '-'}",
            reverse("bill_detail", args=[bill.id]),
            "📘"
        )

    # Motions
    motions = Motion.objects.select_related("sponsor").filter(
        Q(title__icontains=query) |
        Q(motion_number__icontains=query) |
        Q(description__icontains=query) |
        Q(decision__icontains=query) |
        Q(sponsor__first_name__icontains=query) |
        Q(sponsor__last_name__icontains=query)
    )[:5]

    for motion in motions:
        add_result(
            results,
            "Motion",
            f"{motion.motion_number} - {motion.title}",
            f"Status: {motion.get_status_display()} | Sponsor: {motion.sponsor or '-'}",
            reverse("motion_detail", args=[motion.id]),
            "📄"
        )

    # Resolutions
    resolutions = Resolution.objects.filter(
        Q(title__icontains=query) |
        Q(resolution_number__icontains=query) |
        Q(description__icontains=query) |
        Q(decision_summary__icontains=query)
    )[:5]

    for resolution in resolutions:
        add_result(
            results,
            "Resolution",
            f"{resolution.resolution_number} - {resolution.title}",
            f"Status: {resolution.get_status_display()}",
            reverse("resolution_detail", args=[resolution.id]),
            "✅"
        )

    # Plenary Sittings
    sittings = PlenarySitting.objects.filter(
        Q(title__icontains=query) |
        Q(sitting_number__icontains=query) |
        Q(venue__icontains=query) |
        Q(description__icontains=query)
    )[:5]

    for sitting in sittings:
        add_result(
            results,
            "Sitting",
            f"{sitting.sitting_number} - {sitting.title}",
            f"{sitting.sitting_date} | {sitting.get_status_display()}",
            reverse("sitting_detail", args=[sitting.id]),
            "🗓️"
        )

    # Documents
    document_filter = Q(title__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)

    if can_manage_sensitive(role):
        documents = DocumentFile.objects.select_related("category").filter(document_filter)[:5]
    else:
        documents = DocumentFile.objects.select_related("category").filter(
            document_filter,
            access_level__in=["public", "internal"]
        )[:5]

    for document in documents:
        add_result(
            results,
            "Document",
            document.title,
            f"{document.category or 'Uncategorized'} | {document.get_access_level_display()}",
            reverse("document_detail", args=[document.id]),
            "📁"
        )

    # Attendance - sensitive enough to keep internal only
    attendance_sessions = AttendanceSession.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(sitting__title__icontains=query) |
        Q(committee__name__icontains=query)
    )[:5]

    for session in attendance_sessions:
        add_result(
            results,
            "Attendance",
            session.title,
            f"{session.get_attendance_type_display()} | {session.attendance_date}",
            reverse("attendance_session_detail", args=[session.id]),
            "📝"
        )

    # Voting
    vote_sessions = VoteSession.objects.filter(
        Q(title__icontains=query) |
        Q(vote_number__icontains=query) |
        Q(description__icontains=query) |
        Q(decision_summary__icontains=query)
    )[:5]

    for vote in vote_sessions:
        add_result(
            results,
            "Vote",
            f"{vote.vote_number} - {vote.title}",
            f"{vote.get_vote_type_display()} | Outcome: {vote.get_outcome_display()}",
            reverse("vote_session_detail", args=[vote.id]),
            "🗳️"
        )

    # Officials Gallery
    officials = OfficialProfile.objects.select_related(
        "constituency",
        "political_party"
    ).filter(
        Q(full_name__icontains=query) |
        Q(position_title__icontains=query) |
        Q(short_biography__icontains=query) |
        Q(constituency__name__icontains=query) |
        Q(political_party__name__icontains=query) |
        Q(political_party__abbreviation__icontains=query)
    )[:5]

    for official in officials:
        add_result(
            results,
            "Official",
            official.full_name,
            f"{official.position_title} | {official.get_status_display()}",
            reverse("official_detail", args=[official.id]),
            "🖼️"
        )

    log_audit(
        request,
        AuditLog.ACTION_SEARCH,
        "Master Search",
        f"Searched for: {query}"
    )

    return JsonResponse({"results": results[:30]})