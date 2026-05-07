from django.contrib import messages
from django.db.models import Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import get_client_ip, log_audit

from .forms import DocumentCategoryForm, DocumentFileForm, DocumentVersionForm
from .models import (
    DocumentAccessLog,
    DocumentCategory,
    DocumentFile,
    DocumentVersion,
)


def can_access_document(user, document):
    if document.access_level == DocumentFile.ACCESS_PUBLIC and document.is_published:
        return True

    if not user.is_authenticated:
        return False

    profile = getattr(user, "profile", None)

    if not profile:
        return False

    if profile.role in [
        "super_admin",
        "speaker",
        "deputy_speaker",
        "clerk",
        "deputy_clerk",
        "committee_clerk",
        "honourable_member",
        "director_admin_staff",
        "media_pro",
    ]:
        if document.access_level in [
            DocumentFile.ACCESS_INTERNAL,
            DocumentFile.ACCESS_PUBLIC,
        ]:
            return True

    if profile.role in ["super_admin", "clerk", "deputy_clerk"]:
        return True

    return False


def log_document_access(request, document, action):
    DocumentAccessLog.objects.create(
        document=document,
        user=request.user if request.user.is_authenticated else None,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


@legislative_staff_required
def document_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    access_level = request.GET.get("access", "").strip()

    documents = DocumentFile.objects.select_related(
        "category",
        "uploaded_by",
    ).annotate(total_versions=Count("versions"))

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_id:
        documents = documents.filter(category_id=category_id)

    if access_level:
        documents = documents.filter(access_level=access_level)

    return render(request, "documents/document_list.html", {
        "page_title": "Document Library",
        "documents": documents,
        "categories": DocumentCategory.objects.filter(is_active=True),
        "query": query,
        "category_id": category_id,
        "access_level": access_level,
        "access_choices": DocumentFile.ACCESS_CHOICES,
    })


@legislative_staff_required
def document_detail(request, pk):
    document = get_object_or_404(
        DocumentFile.objects.select_related("category", "uploaded_by")
        .prefetch_related("versions", "access_logs"),
        pk=pk
    )

    if not can_access_document(request.user, document):
        log_audit(
            request,
            AuditLog.ACTION_PERMISSION_DENIED,
            "Documents",
            f"Blocked access to document: {document}",
            document
        )
        messages.error(request, "You do not have permission to access this document.")
        return redirect("document_list")

    log_document_access(request, document, DocumentAccessLog.ACTION_VIEW)

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Documents",
        f"Viewed document: {document}",
        document
    )

    return render(request, "documents/document_detail.html", {
        "page_title": document.title,
        "document": document,
    })


@clerk_or_admin_required
def document_create(request):
    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Documents",
                f"Uploaded document: {document}",
                document
            )

            messages.success(request, "Document uploaded successfully.")
            return redirect("document_detail", pk=document.pk)
    else:
        form = DocumentFileForm()

    return render(request, "documents/document_form.html", {
        "page_title": "Upload Document",
        "form": form,
        "form_title": "Upload Document",
    })


@clerk_or_admin_required
def document_update(request, pk):
    document = get_object_or_404(DocumentFile, pk=pk)

    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES, instance=document)

        if form.is_valid():
            document = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Documents",
                f"Updated document: {document}",
                document
            )

            messages.success(request, "Document updated successfully.")
            return redirect("document_detail", pk=document.pk)
    else:
        form = DocumentFileForm(instance=document)

    return render(request, "documents/document_form.html", {
        "page_title": "Update Document",
        "form": form,
        "form_title": "Update Document",
    })


@clerk_or_admin_required
def document_toggle_publish(request, pk):
    document = get_object_or_404(DocumentFile, pk=pk)
    document.is_published = not document.is_published
    document.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Documents",
        f"Toggled publish status for document: {document}",
        document
    )

    messages.success(request, "Document publish status updated successfully.")
    return redirect("document_detail", pk=document.pk)


@clerk_or_admin_required
def document_add_version(request, document_id):
    document = get_object_or_404(DocumentFile, pk=document_id)

    if request.method == "POST":
        form = DocumentVersionForm(request.POST, request.FILES)

        if form.is_valid():
            version = form.save(commit=False)
            version.document = document
            version.uploaded_by = request.user
            version.save()

            if version.version_number > document.version_number:
                document.version_number = version.version_number
                document.file = version.file
                document.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Document Versions",
                f"Added new version for document: {document}",
                version
            )

            messages.success(request, "Document version added successfully.")
            return redirect("document_detail", pk=document.pk)
    else:
        next_version = document.version_number + 1
        form = DocumentVersionForm(initial={"version_number": next_version})

    return render(request, "documents/version_form.html", {
        "page_title": "Add Document Version",
        "document": document,
        "form": form,
        "form_title": f"Add Version for {document.title}",
    })


@legislative_staff_required
def document_download(request, pk):
    document = get_object_or_404(DocumentFile, pk=pk)

    if not can_access_document(request.user, document):
        log_audit(
            request,
            AuditLog.ACTION_PERMISSION_DENIED,
            "Documents",
            f"Blocked download for document: {document}",
            document
        )
        messages.error(request, "You do not have permission to download this document.")
        return redirect("document_list")

    if not document.file:
        raise Http404("File not found.")

    log_document_access(request, document, DocumentAccessLog.ACTION_DOWNLOAD)

    log_audit(
        request,
        AuditLog.ACTION_DOWNLOAD,
        "Documents",
        f"Downloaded document: {document}",
        document
    )

    return FileResponse(document.file.open("rb"), as_attachment=True)


@clerk_or_admin_required
def category_list(request):
    categories = DocumentCategory.objects.annotate(total_documents=Count("documents"))

    return render(request, "documents/category_list.html", {
        "page_title": "Document Categories",
        "categories": categories,
    })


@clerk_or_admin_required
def category_create(request):
    if request.method == "POST":
        form = DocumentCategoryForm(request.POST)

        if form.is_valid():
            category = form.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Document Categories",
                f"Created document category: {category}",
                category
            )

            messages.success(request, "Document category created successfully.")
            return redirect("category_list")
    else:
        form = DocumentCategoryForm()

    return render(request, "documents/category_form.html", {
        "page_title": "Create Document Category",
        "form": form,
        "form_title": "Create Document Category",
    })


@clerk_or_admin_required
def category_update(request, pk):
    category = get_object_or_404(DocumentCategory, pk=pk)

    if request.method == "POST":
        form = DocumentCategoryForm(request.POST, instance=category)

        if form.is_valid():
            category = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Document Categories",
                f"Updated document category: {category}",
                category
            )

            messages.success(request, "Document category updated successfully.")
            return redirect("category_list")
    else:
        form = DocumentCategoryForm(instance=category)

    return render(request, "documents/category_form.html", {
        "page_title": "Update Document Category",
        "form": form,
        "form_title": "Update Document Category",
    })