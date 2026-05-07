from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit
from members.models import HonourableMember

from .forms import BulkVoteForm, VoteRecordForm, VoteSessionForm
from .models import VoteRecord, VoteSession


@legislative_staff_required
def vote_session_list(request):
    query = request.GET.get("q", "").strip()
    vote_type = request.GET.get("type", "").strip()
    outcome = request.GET.get("outcome", "").strip()

    sessions = VoteSession.objects.select_related(
        "sitting",
        "bill",
        "motion",
        "resolution",
        "created_by",
    ).annotate(total_records=Count("records"))

    if query:
        sessions = sessions.filter(
            Q(title__icontains=query) |
            Q(vote_number__icontains=query) |
            Q(description__icontains=query) |
            Q(decision_summary__icontains=query) |
            Q(bill__title__icontains=query) |
            Q(motion__title__icontains=query) |
            Q(resolution__title__icontains=query) |
            Q(sitting__title__icontains=query)
        )

    if vote_type:
        sessions = sessions.filter(vote_type=vote_type)

    if outcome:
        sessions = sessions.filter(outcome=outcome)

    return render(request, "voting/session_list.html", {
        "page_title": "Electronic Voting",
        "sessions": sessions,
        "query": query,
        "vote_type": vote_type,
        "outcome": outcome,
        "type_choices": VoteSession.TYPE_CHOICES,
        "outcome_choices": VoteSession.OUTCOME_CHOICES,
    })


@legislative_staff_required
def vote_session_detail(request, pk):
    session = get_object_or_404(
        VoteSession.objects.select_related(
            "sitting",
            "bill",
            "motion",
            "resolution",
            "created_by",
        ).prefetch_related("records__member"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Voting",
        f"Viewed vote session: {session}",
        session
    )

    return render(request, "voting/session_detail.html", {
        "page_title": session.title,
        "session": session,
        "yes_count": session.records.filter(choice="yes").count(),
        "no_count": session.records.filter(choice="no").count(),
        "abstain_count": session.records.filter(choice="abstain").count(),
        "total_votes": session.records.count(),
    })


@clerk_or_admin_required
def vote_session_create(request):
    if request.method == "POST":
        form = VoteSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Voting",
                f"Created vote session: {session}",
                session
            )

            messages.success(request, "Vote session created successfully.")
            return redirect("vote_session_detail", pk=session.pk)
    else:
        form = VoteSessionForm()

    return render(request, "voting/session_form.html", {
        "page_title": "Create Vote Session",
        "form": form,
        "form_title": "Create Vote Session",
    })


@clerk_or_admin_required
def vote_session_update(request, pk):
    session = get_object_or_404(VoteSession, pk=pk)

    if request.method == "POST":
        form = VoteSessionForm(request.POST, instance=session)

        if form.is_valid():
            session = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Voting",
                f"Updated vote session: {session}",
                session
            )

            messages.success(request, "Vote session updated successfully.")
            return redirect("vote_session_detail", pk=session.pk)
    else:
        form = VoteSessionForm(instance=session)

    return render(request, "voting/session_form.html", {
        "page_title": "Update Vote Session",
        "form": form,
        "form_title": "Update Vote Session",
    })


@clerk_or_admin_required
def vote_session_toggle_lock(request, pk):
    session = get_object_or_404(VoteSession, pk=pk)
    session.is_locked = not session.is_locked
    session.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Voting",
        f"Toggled vote lock status: {session}",
        session
    )

    messages.success(request, "Vote lock status updated successfully.")
    return redirect("vote_session_detail", pk=session.pk)


@clerk_or_admin_required
def vote_session_toggle_open(request, pk):
    session = get_object_or_404(VoteSession, pk=pk)
    session.is_open = not session.is_open
    session.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Voting",
        f"Toggled vote open status: {session}",
        session
    )

    messages.success(request, "Vote open status updated successfully.")
    return redirect("vote_session_detail", pk=session.pk)


@clerk_or_admin_required
def vote_session_toggle_public(request, pk):
    session = get_object_or_404(VoteSession, pk=pk)
    session.is_public = not session.is_public
    session.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Voting",
        f"Toggled vote public status: {session}",
        session
    )

    messages.success(request, "Vote public status updated successfully.")
    return redirect("vote_session_detail", pk=session.pk)


@clerk_or_admin_required
def vote_add_record(request, session_id):
    session = get_object_or_404(VoteSession, pk=session_id)

    if session.is_locked:
        messages.error(request, "This vote session is locked and cannot be edited.")
        return redirect("vote_session_detail", pk=session.pk)

    if not session.is_open:
        messages.error(request, "This vote session is closed.")
        return redirect("vote_session_detail", pk=session.pk)

    if request.method == "POST":
        form = VoteRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.session = session

            existing = VoteRecord.objects.filter(
                session=session,
                member=record.member
            ).first()

            if existing:
                messages.error(
                    request,
                    "This member has already voted in this vote session. Please edit the existing vote record instead."
                )
                return redirect("vote_session_detail", pk=session.pk)

            record.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Vote Records",
                f"Added vote record: {record}",
                record
            )

            messages.success(request, "Vote record added successfully.")
            return redirect("vote_session_detail", pk=session.pk)
    else:
        form = VoteRecordForm()

    return render(request, "voting/record_form.html", {
        "page_title": "Add Vote Record",
        "session": session,
        "form": form,
        "form_title": f"Add Vote Record for {session.vote_number}",
    })


@clerk_or_admin_required
def vote_update_record(request, pk):
    record = get_object_or_404(
        VoteRecord.objects.select_related("session", "member"),
        pk=pk
    )

    if record.session.is_locked:
        messages.error(request, "This vote session is locked and cannot be edited.")
        return redirect("vote_session_detail", pk=record.session.pk)

    if not record.session.is_open:
        messages.error(request, "This vote session is closed.")
        return redirect("vote_session_detail", pk=record.session.pk)

    if request.method == "POST":
        form = VoteRecordForm(request.POST, instance=record)

        if form.is_valid():
            record = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Vote Records",
                f"Updated vote record: {record}",
                record
            )

            messages.success(request, "Vote record updated successfully.")
            return redirect("vote_session_detail", pk=record.session.pk)
    else:
        form = VoteRecordForm(instance=record)

    return render(request, "voting/record_form.html", {
        "page_title": "Update Vote Record",
        "session": record.session,
        "form": form,
        "form_title": "Update Vote Record",
    })


@clerk_or_admin_required
def vote_bulk_mark(request, session_id):
    session = get_object_or_404(VoteSession, pk=session_id)

    if session.is_locked:
        messages.error(request, "This vote session is locked and cannot be edited.")
        return redirect("vote_session_detail", pk=session.pk)

    if not session.is_open:
        messages.error(request, "This vote session is closed.")
        return redirect("vote_session_detail", pk=session.pk)

    members = HonourableMember.objects.filter(status="active").order_by("last_name", "first_name")

    if request.method == "POST":
        form = BulkVoteForm(request.POST, members=members)

        if form.is_valid():
            for member in members:
                choice = form.cleaned_data.get(f"member_{member.id}")
                remarks = form.cleaned_data.get(f"remarks_{member.id}", "")

                VoteRecord.objects.update_or_create(
                    session=session,
                    member=member,
                    defaults={
                        "choice": choice,
                        "remarks": remarks,
                    }
                )

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Vote Records",
                f"Bulk marked votes for session: {session}",
                session
            )

            messages.success(request, "Bulk votes saved successfully.")
            return redirect("vote_session_detail", pk=session.pk)
    else:
        initial = {}

        existing_records = VoteRecord.objects.filter(session=session)
        existing_map = {record.member_id: record for record in existing_records}

        for member in members:
            existing = existing_map.get(member.id)

            if existing:
                initial[f"member_{member.id}"] = existing.choice
                initial[f"remarks_{member.id}"] = existing.remarks

        form = BulkVoteForm(initial=initial, members=members)

    return render(request, "voting/bulk_mark.html", {
        "page_title": "Bulk Mark Votes",
        "session": session,
        "form": form,
        "members": members,
    })


@clerk_or_admin_required
def vote_compute_outcome(request, pk):
    session = get_object_or_404(VoteSession, pk=pk)

    yes_count = session.records.filter(choice="yes").count()
    no_count = session.records.filter(choice="no").count()

    if yes_count > no_count:
        session.outcome = VoteSession.OUTCOME_CARRIED
    elif no_count > yes_count:
        session.outcome = VoteSession.OUTCOME_NEGATIVED
    else:
        session.outcome = VoteSession.OUTCOME_TIED

    session.decision_summary = (
        f"Vote computed automatically. Yes: {yes_count}, "
        f"No: {no_count}, Abstain: {session.records.filter(choice='abstain').count()}."
    )
    session.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Voting",
        f"Computed vote outcome: {session}",
        session
    )

    messages.success(request, "Vote outcome computed successfully.")
    return redirect("vote_session_detail", pk=session.pk)


@legislative_staff_required
def vote_report(request):
    member_id = request.GET.get("member", "").strip()
    vote_type = request.GET.get("type", "").strip()
    choice = request.GET.get("choice", "").strip()

    records = VoteRecord.objects.select_related(
        "session",
        "member",
        "session__bill",
        "session__motion",
        "session__resolution",
        "session__sitting",
    )

    if member_id:
        records = records.filter(member_id=member_id)

    if vote_type:
        records = records.filter(session__vote_type=vote_type)

    if choice:
        records = records.filter(choice=choice)

    members = HonourableMember.objects.filter(status="active").order_by("last_name", "first_name")
    summary = records.values("choice").annotate(total=Count("id"))

    return render(request, "voting/report.html", {
        "page_title": "Voting Report",
        "records": records,
        "members": members,
        "member_id": member_id,
        "vote_type": vote_type,
        "choice": choice,
        "type_choices": VoteSession.TYPE_CHOICES,
        "choice_choices": VoteRecord.CHOICE_CHOICES,
        "summary": summary,
    })