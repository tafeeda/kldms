from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import (
    HansardTranscriptForm,
    OrderPaperForm,
    PlenarySittingForm,
    SittingAgendaItemForm,
    SittingDocumentForm,
    VotesProceedingForm,
)
from .models import (
    HansardTranscript,
    OrderPaper,
    PlenarySitting,
    SittingAgendaItem,
    SittingDocument,
    VotesProceeding,
)


@legislative_staff_required
def sitting_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    sittings = PlenarySitting.objects.select_related("created_by")

    if query:
        sittings = sittings.filter(
            Q(title__icontains=query) |
            Q(sitting_number__icontains=query) |
            Q(venue__icontains=query) |
            Q(description__icontains=query)
        )

    if status:
        sittings = sittings.filter(status=status)

    return render(request, "sittings/sitting_list.html", {
        "page_title": "Plenary Sittings",
        "sittings": sittings,
        "query": query,
        "status": status,
        "status_choices": PlenarySitting.STATUS_CHOICES,
    })


@legislative_staff_required
def sitting_detail(request, pk):
    sitting = get_object_or_404(
        PlenarySitting.objects.select_related("created_by")
        .prefetch_related("agenda_items", "documents"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Plenary Sittings",
        f"Viewed sitting: {sitting}",
        sitting
    )

    return render(request, "sittings/sitting_detail.html", {
        "page_title": sitting.title,
        "sitting": sitting,
    })


@clerk_or_admin_required
def sitting_create(request):
    if request.method == "POST":
        form = PlenarySittingForm(request.POST)

        if form.is_valid():
            sitting = form.save(commit=False)
            sitting.created_by = request.user
            sitting.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Plenary Sittings",
                f"Created sitting: {sitting}",
                sitting
            )

            messages.success(request, "Plenary sitting created successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = PlenarySittingForm()

    return render(request, "sittings/sitting_form.html", {
        "page_title": "Create Plenary Sitting",
        "form": form,
        "form_title": "Create Plenary Sitting",
    })


@clerk_or_admin_required
def sitting_update(request, pk):
    sitting = get_object_or_404(PlenarySitting, pk=pk)

    if request.method == "POST":
        form = PlenarySittingForm(request.POST, instance=sitting)

        if form.is_valid():
            sitting = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Plenary Sittings",
                f"Updated sitting: {sitting}",
                sitting
            )

            messages.success(request, "Plenary sitting updated successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = PlenarySittingForm(instance=sitting)

    return render(request, "sittings/sitting_form.html", {
        "page_title": "Update Plenary Sitting",
        "form": form,
        "form_title": "Update Plenary Sitting",
    })


@clerk_or_admin_required
def sitting_toggle_public(request, pk):
    sitting = get_object_or_404(PlenarySitting, pk=pk)
    sitting.is_public = not sitting.is_public
    sitting.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Plenary Sittings",
        f"Toggled public status for sitting: {sitting}",
        sitting
    )

    messages.success(request, "Sitting public status updated successfully.")
    return redirect("sitting_detail", pk=sitting.pk)


@clerk_or_admin_required
def agenda_add(request, sitting_id):
    sitting = get_object_or_404(PlenarySitting, pk=sitting_id)

    if request.method == "POST":
        form = SittingAgendaItemForm(request.POST)

        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.sitting = sitting
            agenda.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Sitting Agenda",
                f"Added agenda item to sitting: {sitting}",
                agenda
            )

            messages.success(request, "Agenda item added successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = SittingAgendaItemForm()

    return render(request, "sittings/agenda_form.html", {
        "page_title": "Add Agenda Item",
        "sitting": sitting,
        "form": form,
        "form_title": f"Add Agenda Item for {sitting.sitting_number}",
    })


@clerk_or_admin_required
def agenda_update(request, pk):
    agenda = get_object_or_404(SittingAgendaItem.objects.select_related("sitting"), pk=pk)

    if request.method == "POST":
        form = SittingAgendaItemForm(request.POST, instance=agenda)

        if form.is_valid():
            agenda = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Sitting Agenda",
                f"Updated agenda item: {agenda}",
                agenda
            )

            messages.success(request, "Agenda item updated successfully.")
            return redirect("sitting_detail", pk=agenda.sitting.pk)
    else:
        form = SittingAgendaItemForm(instance=agenda)

    return render(request, "sittings/agenda_form.html", {
        "page_title": "Update Agenda Item",
        "sitting": agenda.sitting,
        "form": form,
        "form_title": "Update Agenda Item",
    })


@clerk_or_admin_required
def order_paper_manage(request, sitting_id):
    sitting = get_object_or_404(PlenarySitting, pk=sitting_id)
    order_paper = getattr(sitting, "order_paper", None)

    if request.method == "POST":
        form = OrderPaperForm(request.POST, request.FILES, instance=order_paper)

        if form.is_valid():
            paper = form.save(commit=False)
            paper.sitting = sitting
            paper.prepared_by = request.user
            paper.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE if order_paper else AuditLog.ACTION_CREATE,
                "Order Papers",
                f"Saved order paper for sitting: {sitting}",
                paper
            )

            messages.success(request, "Order paper saved successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = OrderPaperForm(instance=order_paper)

    return render(request, "sittings/order_paper_form.html", {
        "page_title": "Manage Order Paper",
        "sitting": sitting,
        "form": form,
        "form_title": f"Order Paper for {sitting.sitting_number}",
    })


@clerk_or_admin_required
def votes_proceeding_manage(request, sitting_id):
    sitting = get_object_or_404(PlenarySitting, pk=sitting_id)
    votes_proceeding = getattr(sitting, "votes_proceeding", None)

    if request.method == "POST":
        form = VotesProceedingForm(request.POST, request.FILES, instance=votes_proceeding)

        if form.is_valid():
            proceeding = form.save(commit=False)
            proceeding.sitting = sitting
            proceeding.prepared_by = request.user
            proceeding.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE if votes_proceeding else AuditLog.ACTION_CREATE,
                "Votes and Proceedings",
                f"Saved votes and proceedings for sitting: {sitting}",
                proceeding
            )

            messages.success(request, "Votes and proceedings saved successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = VotesProceedingForm(instance=votes_proceeding)

    return render(request, "sittings/votes_proceeding_form.html", {
        "page_title": "Manage Votes and Proceedings",
        "sitting": sitting,
        "form": form,
        "form_title": f"Votes and Proceedings for {sitting.sitting_number}",
    })


@clerk_or_admin_required
def hansard_manage(request, sitting_id):
    sitting = get_object_or_404(PlenarySitting, pk=sitting_id)
    hansard = getattr(sitting, "hansard", None)

    if request.method == "POST":
        form = HansardTranscriptForm(request.POST, request.FILES, instance=hansard)

        if form.is_valid():
            transcript = form.save(commit=False)
            transcript.sitting = sitting
            transcript.prepared_by = request.user
            transcript.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE if hansard else AuditLog.ACTION_CREATE,
                "Hansard",
                f"Saved hansard for sitting: {sitting}",
                transcript
            )

            messages.success(request, "Hansard/transcript saved successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = HansardTranscriptForm(instance=hansard)

    return render(request, "sittings/hansard_form.html", {
        "page_title": "Manage Hansard",
        "sitting": sitting,
        "form": form,
        "form_title": f"Hansard for {sitting.sitting_number}",
    })


@clerk_or_admin_required
def sitting_upload_document(request, sitting_id):
    sitting = get_object_or_404(PlenarySitting, pk=sitting_id)

    if request.method == "POST":
        form = SittingDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.sitting = sitting
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Sitting Documents",
                f"Uploaded sitting document: {document}",
                document
            )

            messages.success(request, "Sitting document uploaded successfully.")
            return redirect("sitting_detail", pk=sitting.pk)
    else:
        form = SittingDocumentForm()

    return render(request, "sittings/sitting_document_form.html", {
        "page_title": "Upload Sitting Document",
        "sitting": sitting,
        "form": form,
        "form_title": f"Upload Document for {sitting.sitting_number}",
    })


@clerk_or_admin_required
def sitting_toggle_document_public(request, pk):
    document = get_object_or_404(SittingDocument.objects.select_related("sitting"), pk=pk)
    document.is_public = not document.is_public
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Sitting Documents",
        f"Toggled public status for sitting document: {document}",
        document
    )

    messages.success(request, "Document public status updated successfully.")
    return redirect("sitting_detail", pk=document.sitting.pk)