from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import CommitteeDocumentForm, CommitteeForm, CommitteeMembershipForm
from .models import Committee, CommitteeDocument, CommitteeMembership


@legislative_staff_required
def committee_list(request):
    query = request.GET.get("q", "").strip()

    committees = Committee.objects.select_related(
        "chairman",
        "vice_chairman",
        "committee_clerk",
    ).prefetch_related("memberships")

    if query:
        committees = committees.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(chairman__first_name__icontains=query) |
            Q(chairman__last_name__icontains=query) |
            Q(vice_chairman__first_name__icontains=query) |
            Q(vice_chairman__last_name__icontains=query)
        )

    context = {
        "page_title": "Committees",
        "committees": committees,
        "query": query,
    }
    return render(request, "committees/committee_list.html", context)


@legislative_staff_required
def committee_detail(request, pk):
    committee = get_object_or_404(
        Committee.objects.select_related(
            "chairman",
            "vice_chairman",
            "committee_clerk",
        ).prefetch_related(
            "memberships__member",
            "documents",
        ),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Committees",
        f"Viewed committee: {committee}",
        committee
    )

    return render(request, "committees/committee_detail.html", {
        "page_title": committee.name,
        "committee": committee,
    })


@clerk_or_admin_required
def committee_create(request):
    if request.method == "POST":
        form = CommitteeForm(request.POST)

        if form.is_valid():
            committee = form.save(commit=False)
            committee.created_by = request.user
            committee.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Committees",
                f"Created committee: {committee}",
                committee
            )

            messages.success(request, "Committee created successfully.")
            return redirect("committee_detail", pk=committee.pk)
    else:
        form = CommitteeForm()

    return render(request, "committees/committee_form.html", {
        "page_title": "Create Committee",
        "form": form,
        "form_title": "Create Committee",
    })


@clerk_or_admin_required
def committee_update(request, pk):
    committee = get_object_or_404(Committee, pk=pk)

    if request.method == "POST":
        form = CommitteeForm(request.POST, instance=committee)

        if form.is_valid():
            committee = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Committees",
                f"Updated committee: {committee}",
                committee
            )

            messages.success(request, "Committee updated successfully.")
            return redirect("committee_detail", pk=committee.pk)
    else:
        form = CommitteeForm(instance=committee)

    return render(request, "committees/committee_form.html", {
        "page_title": "Update Committee",
        "form": form,
        "form_title": "Update Committee",
    })


@clerk_or_admin_required
def committee_add_member(request, committee_id):
    committee = get_object_or_404(Committee, pk=committee_id)

    if request.method == "POST":
        form = CommitteeMembershipForm(request.POST)

        if form.is_valid():
            membership = form.save(commit=False)
            membership.committee = committee

            existing = CommitteeMembership.objects.filter(
                committee=committee,
                member=membership.member
            ).first()

            if existing:
                messages.error(
                    request,
                    "This honourable member is already added to this committee. You can edit the existing membership instead."
                )
                return redirect("committee_detail", pk=committee.pk)

            membership.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Committee Membership",
                f"Added {membership.member} to {committee}",
                membership
            )

            messages.success(request, "Member added to committee successfully.")
            return redirect("committee_detail", pk=committee.pk)
    else:
        form = CommitteeMembershipForm()

    return render(request, "committees/committee_membership_form.html", {
        "page_title": "Add Committee Member",
        "committee": committee,
        "form": form,
        "form_title": f"Add Member to {committee.name}",
    })


@clerk_or_admin_required
def committee_update_member(request, pk):
    membership = get_object_or_404(
        CommitteeMembership.objects.select_related("committee", "member"),
        pk=pk
    )

    if request.method == "POST":
        form = CommitteeMembershipForm(request.POST, instance=membership)

        if form.is_valid():
            membership = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Committee Membership",
                f"Updated committee membership: {membership}",
                membership
            )

            messages.success(request, "Committee membership updated successfully.")
            return redirect("committee_detail", pk=membership.committee.pk)
    else:
        form = CommitteeMembershipForm(instance=membership)

    return render(request, "committees/committee_membership_form.html", {
        "page_title": "Update Committee Member",
        "committee": membership.committee,
        "form": form,
        "form_title": "Update Committee Member",
    })


@clerk_or_admin_required
def committee_remove_member(request, pk):
    membership = get_object_or_404(
        CommitteeMembership.objects.select_related("committee", "member"),
        pk=pk
    )
    committee_pk = membership.committee.pk
    member_name = str(membership.member)

    log_audit(
        request,
        AuditLog.ACTION_DELETE,
        "Committee Membership",
        f"Removed {member_name} from {membership.committee}",
        membership
    )

    membership.delete()
    messages.success(request, "Member removed from committee successfully.")
    return redirect("committee_detail", pk=committee_pk)


@clerk_or_admin_required
def committee_upload_document(request, committee_id):
    committee = get_object_or_404(Committee, pk=committee_id)

    if request.method == "POST":
        form = CommitteeDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.committee = committee
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Committee Documents",
                f"Uploaded committee document: {document}",
                document
            )

            messages.success(request, "Committee document uploaded successfully.")
            return redirect("committee_detail", pk=committee.pk)
    else:
        form = CommitteeDocumentForm()

    return render(request, "committees/committee_document_form.html", {
        "page_title": "Upload Committee Document",
        "committee": committee,
        "form": form,
        "form_title": f"Upload Document for {committee.name}",
    })


@clerk_or_admin_required
def committee_toggle_document_publish(request, pk):
    document = get_object_or_404(CommitteeDocument.objects.select_related("committee"), pk=pk)
    document.is_published = not document.is_published
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Committee Documents",
        f"Toggled publish status for document: {document}",
        document
    )

    messages.success(request, "Document publish status updated successfully.")
    return redirect("committee_detail", pk=document.committee.pk)