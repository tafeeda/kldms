from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit
from committees.models import CommitteeMembership
from members.models import HonourableMember

from .forms import AttendanceBulkRecordForm, AttendanceRecordForm, AttendanceSessionForm
from .models import AttendanceRecord, AttendanceSession


@legislative_staff_required
def attendance_session_list(request):
    query = request.GET.get("q", "").strip()
    attendance_type = request.GET.get("type", "").strip()

    sessions = AttendanceSession.objects.select_related(
        "sitting",
        "committee",
        "recorded_by",
    ).annotate(total_records=Count("records"))

    if query:
        sessions = sessions.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(sitting__title__icontains=query) |
            Q(committee__name__icontains=query)
        )

    if attendance_type:
        sessions = sessions.filter(attendance_type=attendance_type)

    return render(request, "attendance/session_list.html", {
        "page_title": "Attendance",
        "sessions": sessions,
        "query": query,
        "attendance_type": attendance_type,
        "type_choices": AttendanceSession.TYPE_CHOICES,
    })


@legislative_staff_required
def attendance_session_detail(request, pk):
    session = get_object_or_404(
        AttendanceSession.objects.select_related("sitting", "committee", "recorded_by")
        .prefetch_related("records__member"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Attendance",
        f"Viewed attendance session: {session}",
        session
    )

    return render(request, "attendance/session_detail.html", {
        "page_title": session.title,
        "session": session,
        "present_count": session.records.filter(status="present").count(),
        "absent_count": session.records.filter(status="absent").count(),
        "late_count": session.records.filter(status="late").count(),
        "excused_count": session.records.filter(status="excused").count(),
    })


@clerk_or_admin_required
def attendance_session_create(request):
    if request.method == "POST":
        form = AttendanceSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.recorded_by = request.user
            session.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Attendance",
                f"Created attendance session: {session}",
                session
            )

            messages.success(request, "Attendance session created successfully.")
            return redirect("attendance_session_detail", pk=session.pk)
    else:
        form = AttendanceSessionForm()

    return render(request, "attendance/session_form.html", {
        "page_title": "Create Attendance Session",
        "form": form,
        "form_title": "Create Attendance Session",
    })


@clerk_or_admin_required
def attendance_session_update(request, pk):
    session = get_object_or_404(AttendanceSession, pk=pk)

    if request.method == "POST":
        form = AttendanceSessionForm(request.POST, instance=session)

        if form.is_valid():
            session = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Attendance",
                f"Updated attendance session: {session}",
                session
            )

            messages.success(request, "Attendance session updated successfully.")
            return redirect("attendance_session_detail", pk=session.pk)
    else:
        form = AttendanceSessionForm(instance=session)

    return render(request, "attendance/session_form.html", {
        "page_title": "Update Attendance Session",
        "form": form,
        "form_title": "Update Attendance Session",
    })


@clerk_or_admin_required
def attendance_toggle_lock(request, pk):
    session = get_object_or_404(AttendanceSession, pk=pk)
    session.is_locked = not session.is_locked
    session.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Attendance",
        f"Toggled attendance lock status: {session}",
        session
    )

    messages.success(request, "Attendance lock status updated successfully.")
    return redirect("attendance_session_detail", pk=session.pk)


@clerk_or_admin_required
def attendance_add_record(request, session_id):
    session = get_object_or_404(AttendanceSession, pk=session_id)

    if session.is_locked:
        messages.error(request, "This attendance session is locked and cannot be edited.")
        return redirect("attendance_session_detail", pk=session.pk)

    if request.method == "POST":
        form = AttendanceRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.session = session

            existing = AttendanceRecord.objects.filter(
                session=session,
                member=record.member
            ).first()

            if existing:
                messages.error(
                    request,
                    "This member already has an attendance record for this session. Please edit the existing record instead."
                )
                return redirect("attendance_session_detail", pk=session.pk)

            record.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Attendance Records",
                f"Added attendance record: {record}",
                record
            )

            messages.success(request, "Attendance record added successfully.")
            return redirect("attendance_session_detail", pk=session.pk)
    else:
        form = AttendanceRecordForm()

    return render(request, "attendance/record_form.html", {
        "page_title": "Add Attendance Record",
        "session": session,
        "form": form,
        "form_title": f"Add Record for {session.title}",
    })


@clerk_or_admin_required
def attendance_update_record(request, pk):
    record = get_object_or_404(
        AttendanceRecord.objects.select_related("session", "member"),
        pk=pk
    )

    if record.session.is_locked:
        messages.error(request, "This attendance session is locked and cannot be edited.")
        return redirect("attendance_session_detail", pk=record.session.pk)

    if request.method == "POST":
        form = AttendanceRecordForm(request.POST, instance=record)

        if form.is_valid():
            record = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Attendance Records",
                f"Updated attendance record: {record}",
                record
            )

            messages.success(request, "Attendance record updated successfully.")
            return redirect("attendance_session_detail", pk=record.session.pk)
    else:
        form = AttendanceRecordForm(instance=record)

    return render(request, "attendance/record_form.html", {
        "page_title": "Update Attendance Record",
        "session": record.session,
        "form": form,
        "form_title": "Update Attendance Record",
    })


@clerk_or_admin_required
def attendance_bulk_mark(request, session_id):
    session = get_object_or_404(AttendanceSession, pk=session_id)

    if session.is_locked:
        messages.error(request, "This attendance session is locked and cannot be edited.")
        return redirect("attendance_session_detail", pk=session.pk)

    if session.attendance_type == AttendanceSession.TYPE_COMMITTEE and session.committee:
        members = HonourableMember.objects.filter(
            committee_memberships__committee=session.committee,
            committee_memberships__is_active=True,
            status="active",
        ).distinct()
    else:
        members = HonourableMember.objects.filter(status="active")

    if request.method == "POST":
        form = AttendanceBulkRecordForm(request.POST, members=members)

        if form.is_valid():
            for member in members:
                status = form.cleaned_data.get(f"member_{member.id}")
                remarks = form.cleaned_data.get(f"remarks_{member.id}", "")

                AttendanceRecord.objects.update_or_create(
                    session=session,
                    member=member,
                    defaults={
                        "status": status,
                        "remarks": remarks,
                    }
                )

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Attendance Records",
                f"Bulk marked attendance for session: {session}",
                session
            )

            messages.success(request, "Bulk attendance saved successfully.")
            return redirect("attendance_session_detail", pk=session.pk)
    else:
        initial = {}

        existing_records = AttendanceRecord.objects.filter(session=session)
        existing_map = {record.member_id: record for record in existing_records}

        for member in members:
            existing = existing_map.get(member.id)

            if existing:
                initial[f"member_{member.id}"] = existing.status
                initial[f"remarks_{member.id}"] = existing.remarks

        form = AttendanceBulkRecordForm(initial=initial, members=members)

    return render(request, "attendance/bulk_mark.html", {
        "page_title": "Bulk Mark Attendance",
        "session": session,
        "form": form,
        "members": members,
    })


@legislative_staff_required
def attendance_report(request):
    member_id = request.GET.get("member", "").strip()
    attendance_type = request.GET.get("type", "").strip()

    records = AttendanceRecord.objects.select_related(
        "session",
        "member",
        "session__sitting",
        "session__committee",
    )

    if member_id:
        records = records.filter(member_id=member_id)

    if attendance_type:
        records = records.filter(session__attendance_type=attendance_type)

    members = HonourableMember.objects.filter(status="active")

    summary = records.values("status").annotate(total=Count("id"))

    return render(request, "attendance/report.html", {
        "page_title": "Attendance Report",
        "records": records,
        "members": members,
        "member_id": member_id,
        "attendance_type": attendance_type,
        "type_choices": AttendanceSession.TYPE_CHOICES,
        "summary": summary,
    })