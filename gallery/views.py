from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import gallery_manager_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import OfficialProfileForm
from .models import OfficialProfile


def public_official_gallery(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    officials = OfficialProfile.objects.filter(is_published=True).select_related(
        "constituency",
        "political_party",
    )

    if query:
        officials = officials.filter(
            Q(full_name__icontains=query) |
            Q(position_title__icontains=query) |
            Q(short_biography__icontains=query) |
            Q(constituency__name__icontains=query) |
            Q(political_party__name__icontains=query) |
            Q(political_party__abbreviation__icontains=query)
        )

    if category:
        officials = officials.filter(category=category)

    if status:
        officials = officials.filter(status=status)

    return render(request, "gallery/public_gallery.html", {
        "page_title": "Officials Gallery",
        "officials": officials,
        "query": query,
        "category": category,
        "status": status,
        "category_choices": OfficialProfile.CATEGORY_CHOICES,
        "status_choices": OfficialProfile.STATUS_CHOICES,
    })


@legislative_staff_required
def official_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    officials = OfficialProfile.objects.select_related(
        "constituency",
        "political_party",
        "created_by",
    )

    if query:
        officials = officials.filter(
            Q(full_name__icontains=query) |
            Q(position_title__icontains=query) |
            Q(short_biography__icontains=query) |
            Q(constituency__name__icontains=query) |
            Q(political_party__name__icontains=query) |
            Q(political_party__abbreviation__icontains=query)
        )

    if category:
        officials = officials.filter(category=category)

    if status:
        officials = officials.filter(status=status)

    return render(request, "gallery/official_list.html", {
        "page_title": "Officials Gallery Management",
        "officials": officials,
        "query": query,
        "category": category,
        "status": status,
        "category_choices": OfficialProfile.CATEGORY_CHOICES,
        "status_choices": OfficialProfile.STATUS_CHOICES,
    })


@legislative_staff_required
def official_detail(request, pk):
    official = get_object_or_404(
        OfficialProfile.objects.select_related(
            "constituency",
            "political_party",
            "created_by",
        ),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Officials Gallery",
        f"Viewed official profile: {official}",
        official
    )

    return render(request, "gallery/official_detail.html", {
        "page_title": official.full_name,
        "official": official,
    })


@gallery_manager_required
def official_create(request):
    if request.method == "POST":
        form = OfficialProfileForm(request.POST, request.FILES)

        if form.is_valid():
            official = form.save(commit=False)
            official.created_by = request.user
            official.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Officials Gallery",
                f"Created official profile: {official}",
                official
            )

            messages.success(request, "Official profile created successfully.")
            return redirect("official_detail", pk=official.pk)
    else:
        form = OfficialProfileForm()

    return render(request, "gallery/official_form.html", {
        "page_title": "Create Official Profile",
        "form": form,
        "form_title": "Create Official Profile",
    })


@gallery_manager_required
def official_update(request, pk):
    official = get_object_or_404(OfficialProfile, pk=pk)

    if request.method == "POST":
        form = OfficialProfileForm(request.POST, request.FILES, instance=official)

        if form.is_valid():
            official = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Officials Gallery",
                f"Updated official profile: {official}",
                official
            )

            messages.success(request, "Official profile updated successfully.")
            return redirect("official_detail", pk=official.pk)
    else:
        form = OfficialProfileForm(instance=official)

    return render(request, "gallery/official_form.html", {
        "page_title": "Update Official Profile",
        "form": form,
        "form_title": "Update Official Profile",
    })


@gallery_manager_required
def official_toggle_publish(request, pk):
    official = get_object_or_404(OfficialProfile, pk=pk)
    official.is_published = not official.is_published
    official.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Officials Gallery",
        f"Toggled publish status for official: {official}",
        official
    )

    messages.success(request, "Official publish status updated successfully.")
    return redirect("official_detail", pk=official.pk)