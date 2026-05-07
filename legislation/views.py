from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit
from .forms import (
    BillAmendmentForm,
    BillDocumentForm,
    BillForm,
    BillReadingForm,
    MotionDocumentForm,
    MotionForm,
    ResolutionDocumentForm,
    ResolutionForm,
)

from .models import (
    Bill,
    BillAmendment,
    BillDocument,
    BillReading,
    Motion,
    MotionDocument,
    Resolution,
    ResolutionDocument,
)


@legislative_staff_required
def bill_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    bills = Bill.objects.select_related("sponsor", "created_by").prefetch_related("co_sponsors")

    if query:
        bills = bills.filter(
            Q(title__icontains=query) |
            Q(bill_number__icontains=query) |
            Q(summary__icontains=query) |
            Q(long_title__icontains=query) |
            Q(sponsor__first_name__icontains=query) |
            Q(sponsor__last_name__icontains=query)
        )

    if status:
        bills = bills.filter(status=status)

    return render(request, "legislation/bill_list.html", {
        "page_title": "Bills",
        "bills": bills,
        "query": query,
        "status": status,
        "status_choices": Bill.STATUS_CHOICES,
    })


@legislative_staff_required
def bill_detail(request, pk):
    bill = get_object_or_404(
        Bill.objects.select_related("sponsor", "created_by")
        .prefetch_related("co_sponsors", "readings", "amendments", "documents"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Bills",
        f"Viewed bill: {bill}",
        bill
    )

    return render(request, "legislation/bill_detail.html", {
        "page_title": bill.title,
        "bill": bill,
    })


@clerk_or_admin_required
def bill_create(request):
    if request.method == "POST":
        form = BillForm(request.POST)

        if form.is_valid():
            bill = form.save(commit=False)
            bill.created_by = request.user
            bill.save()
            form.save_m2m()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Bills",
                f"Created bill: {bill}",
                bill
            )

            messages.success(request, "Bill created successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillForm()

    return render(request, "legislation/bill_form.html", {
        "page_title": "Create Bill",
        "form": form,
        "form_title": "Create Bill",
    })


@clerk_or_admin_required
def bill_update(request, pk):
    bill = get_object_or_404(Bill, pk=pk)

    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)

        if form.is_valid():
            bill = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Bills",
                f"Updated bill: {bill}",
                bill
            )

            messages.success(request, "Bill updated successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillForm(instance=bill)

    return render(request, "legislation/bill_form.html", {
        "page_title": "Update Bill",
        "form": form,
        "form_title": "Update Bill",
    })


@clerk_or_admin_required
def bill_toggle_public(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    bill.is_public = not bill.is_public
    bill.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Bills",
        f"Toggled public status for bill: {bill}",
        bill
    )

    messages.success(request, "Bill public status updated successfully.")
    return redirect("bill_detail", pk=bill.pk)


@clerk_or_admin_required
def bill_add_reading(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    if request.method == "POST":
        form = BillReadingForm(request.POST)

        if form.is_valid():
            reading = form.save(commit=False)
            reading.bill = bill
            reading.recorded_by = request.user
            reading.save()

            if reading.reading_type == BillReading.READING_FIRST:
                bill.status = Bill.STATUS_FIRST_READING
            elif reading.reading_type == BillReading.READING_SECOND:
                bill.status = Bill.STATUS_SECOND_READING
            elif reading.reading_type == BillReading.READING_THIRD:
                bill.status = Bill.STATUS_THIRD_READING

            bill.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Bill Readings",
                f"Added reading to bill: {bill}",
                reading
            )

            messages.success(request, "Bill reading added successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillReadingForm()

    return render(request, "legislation/bill_reading_form.html", {
        "page_title": "Add Bill Reading",
        "bill": bill,
        "form": form,
        "form_title": f"Add Reading for {bill.bill_number}",
    })


@clerk_or_admin_required
def bill_add_amendment(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    if request.method == "POST":
        form = BillAmendmentForm(request.POST)

        if form.is_valid():
            amendment = form.save(commit=False)
            amendment.bill = bill
            amendment.created_by = request.user
            amendment.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Bill Amendments",
                f"Added amendment to bill: {bill}",
                amendment
            )

            messages.success(request, "Bill amendment added successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillAmendmentForm()

    return render(request, "legislation/bill_amendment_form.html", {
        "page_title": "Add Bill Amendment",
        "bill": bill,
        "form": form,
        "form_title": f"Add Amendment for {bill.bill_number}",
    })


@clerk_or_admin_required
def bill_update_amendment(request, pk):
    amendment = get_object_or_404(BillAmendment.objects.select_related("bill"), pk=pk)

    if request.method == "POST":
        form = BillAmendmentForm(request.POST, instance=amendment)

        if form.is_valid():
            amendment = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Bill Amendments",
                f"Updated amendment: {amendment}",
                amendment
            )

            messages.success(request, "Bill amendment updated successfully.")
            return redirect("bill_detail", pk=amendment.bill.pk)
    else:
        form = BillAmendmentForm(instance=amendment)

    return render(request, "legislation/bill_amendment_form.html", {
        "page_title": "Update Bill Amendment",
        "bill": amendment.bill,
        "form": form,
        "form_title": "Update Bill Amendment",
    })


@clerk_or_admin_required
def bill_upload_document(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    if request.method == "POST":
        form = BillDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.bill = bill
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Bill Documents",
                f"Uploaded bill document: {document}",
                document
            )

            messages.success(request, "Bill document uploaded successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillDocumentForm()

    return render(request, "legislation/bill_document_form.html", {
        "page_title": "Upload Bill Document",
        "bill": bill,
        "form": form,
        "form_title": f"Upload Document for {bill.bill_number}",
    })


@clerk_or_admin_required
def bill_toggle_document_public(request, pk):
    document = get_object_or_404(BillDocument.objects.select_related("bill"), pk=pk)
    document.is_public = not document.is_public
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Bill Documents",
        f"Toggled public status for document: {document}",
        document
    )

    messages.success(request, "Document public status updated successfully.")
    return redirect("bill_detail", pk=document.bill.pk)



@legislative_staff_required
def motion_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    motions = Motion.objects.select_related("sponsor", "created_by").prefetch_related("co_sponsors")

    if query:
        motions = motions.filter(
            Q(title__icontains=query) |
            Q(motion_number__icontains=query) |
            Q(description__icontains=query) |
            Q(decision__icontains=query) |
            Q(sponsor__first_name__icontains=query) |
            Q(sponsor__last_name__icontains=query)
        )

    if status:
        motions = motions.filter(status=status)

    return render(request, "legislation/motion_list.html", {
        "page_title": "Motions",
        "motions": motions,
        "query": query,
        "status": status,
        "status_choices": Motion.STATUS_CHOICES,
    })


@legislative_staff_required
def motion_detail(request, pk):
    motion = get_object_or_404(
        Motion.objects.select_related("sponsor", "created_by")
        .prefetch_related("co_sponsors", "documents", "resolutions"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Motions",
        f"Viewed motion: {motion}",
        motion
    )

    return render(request, "legislation/motion_detail.html", {
        "page_title": motion.title,
        "motion": motion,
    })


@clerk_or_admin_required
def motion_create(request):
    if request.method == "POST":
        form = MotionForm(request.POST)

        if form.is_valid():
            motion = form.save(commit=False)
            motion.created_by = request.user
            motion.save()
            form.save_m2m()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Motions",
                f"Created motion: {motion}",
                motion
            )

            messages.success(request, "Motion created successfully.")
            return redirect("motion_detail", pk=motion.pk)
    else:
        form = MotionForm()

    return render(request, "legislation/motion_form.html", {
        "page_title": "Create Motion",
        "form": form,
        "form_title": "Create Motion",
    })


@clerk_or_admin_required
def motion_update(request, pk):
    motion = get_object_or_404(Motion, pk=pk)

    if request.method == "POST":
        form = MotionForm(request.POST, instance=motion)

        if form.is_valid():
            motion = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Motions",
                f"Updated motion: {motion}",
                motion
            )

            messages.success(request, "Motion updated successfully.")
            return redirect("motion_detail", pk=motion.pk)
    else:
        form = MotionForm(instance=motion)

    return render(request, "legislation/motion_form.html", {
        "page_title": "Update Motion",
        "form": form,
        "form_title": "Update Motion",
    })


@clerk_or_admin_required
def motion_toggle_public(request, pk):
    motion = get_object_or_404(Motion, pk=pk)
    motion.is_public = not motion.is_public
    motion.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Motions",
        f"Toggled public status for motion: {motion}",
        motion
    )

    messages.success(request, "Motion public status updated successfully.")
    return redirect("motion_detail", pk=motion.pk)


@clerk_or_admin_required
def motion_upload_document(request, motion_id):
    motion = get_object_or_404(Motion, pk=motion_id)

    if request.method == "POST":
        form = MotionDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.motion = motion
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Motion Documents",
                f"Uploaded motion document: {document}",
                document
            )

            messages.success(request, "Motion document uploaded successfully.")
            return redirect("motion_detail", pk=motion.pk)
    else:
        form = MotionDocumentForm()

    return render(request, "legislation/motion_document_form.html", {
        "page_title": "Upload Motion Document",
        "motion": motion,
        "form": form,
        "form_title": f"Upload Document for {motion.motion_number}",
    })


@clerk_or_admin_required
def motion_toggle_document_public(request, pk):
    document = get_object_or_404(MotionDocument.objects.select_related("motion"), pk=pk)
    document.is_public = not document.is_public
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Motion Documents",
        f"Toggled public status for motion document: {document}",
        document
    )

    messages.success(request, "Motion document public status updated successfully.")
    return redirect("motion_detail", pk=document.motion.pk)


@legislative_staff_required
def resolution_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    resolutions = Resolution.objects.select_related("related_motion", "created_by")

    if query:
        resolutions = resolutions.filter(
            Q(title__icontains=query) |
            Q(resolution_number__icontains=query) |
            Q(description__icontains=query) |
            Q(decision_summary__icontains=query) |
            Q(related_motion__title__icontains=query) |
            Q(related_motion__motion_number__icontains=query)
        )

    if status:
        resolutions = resolutions.filter(status=status)

    return render(request, "legislation/resolution_list.html", {
        "page_title": "Resolutions",
        "resolutions": resolutions,
        "query": query,
        "status": status,
        "status_choices": Resolution.STATUS_CHOICES,
    })


@legislative_staff_required
def resolution_detail(request, pk):
    resolution = get_object_or_404(
        Resolution.objects.select_related("related_motion", "created_by")
        .prefetch_related("documents"),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Resolutions",
        f"Viewed resolution: {resolution}",
        resolution
    )

    return render(request, "legislation/resolution_detail.html", {
        "page_title": resolution.title,
        "resolution": resolution,
    })


@clerk_or_admin_required
def resolution_create(request):
    if request.method == "POST":
        form = ResolutionForm(request.POST)

        if form.is_valid():
            resolution = form.save(commit=False)
            resolution.created_by = request.user
            resolution.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Resolutions",
                f"Created resolution: {resolution}",
                resolution
            )

            messages.success(request, "Resolution created successfully.")
            return redirect("resolution_detail", pk=resolution.pk)
    else:
        form = ResolutionForm()

    return render(request, "legislation/resolution_form.html", {
        "page_title": "Create Resolution",
        "form": form,
        "form_title": "Create Resolution",
    })


@clerk_or_admin_required
def resolution_update(request, pk):
    resolution = get_object_or_404(Resolution, pk=pk)

    if request.method == "POST":
        form = ResolutionForm(request.POST, instance=resolution)

        if form.is_valid():
            resolution = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Resolutions",
                f"Updated resolution: {resolution}",
                resolution
            )

            messages.success(request, "Resolution updated successfully.")
            return redirect("resolution_detail", pk=resolution.pk)
    else:
        form = ResolutionForm(instance=resolution)

    return render(request, "legislation/resolution_form.html", {
        "page_title": "Update Resolution",
        "form": form,
        "form_title": "Update Resolution",
    })


@clerk_or_admin_required
def resolution_toggle_public(request, pk):
    resolution = get_object_or_404(Resolution, pk=pk)
    resolution.is_public = not resolution.is_public
    resolution.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Resolutions",
        f"Toggled public status for resolution: {resolution}",
        resolution
    )

    messages.success(request, "Resolution public status updated successfully.")
    return redirect("resolution_detail", pk=resolution.pk)


@clerk_or_admin_required
def resolution_upload_document(request, resolution_id):
    resolution = get_object_or_404(Resolution, pk=resolution_id)

    if request.method == "POST":
        form = ResolutionDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.resolution = resolution
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Resolution Documents",
                f"Uploaded resolution document: {document}",
                document
            )

            messages.success(request, "Resolution document uploaded successfully.")
            return redirect("resolution_detail", pk=resolution.pk)
    else:
        form = ResolutionDocumentForm()

    return render(request, "legislation/resolution_document_form.html", {
        "page_title": "Upload Resolution Document",
        "resolution": resolution,
        "form": form,
        "form_title": f"Upload Document for {resolution.resolution_number}",
    })


@clerk_or_admin_required
def resolution_toggle_document_public(request, pk):
    document = get_object_or_404(ResolutionDocument.objects.select_related("resolution"), pk=pk)
    document.is_public = not document.is_public
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Resolution Documents",
        f"Toggled public status for resolution document: {document}",
        document
    )

    messages.success(request, "Resolution document public status updated successfully.")
    return redirect("resolution_detail", pk=document.resolution.pk)