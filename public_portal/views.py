from django.db.models import Q
from django.shortcuts import render

from documents.models import DocumentFile
from legislation.models import Bill, Motion, Resolution
from sittings.models import PlenarySitting


def public_home(request):
    context = {
        "public_bills_count": Bill.objects.filter(is_public=True).count(),
        "public_motions_count": Motion.objects.filter(is_public=True).count(),
        "public_resolutions_count": Resolution.objects.filter(is_public=True).count(),
        "public_sittings_count": PlenarySitting.objects.filter(is_public=True).count(),
        "public_documents_count": DocumentFile.objects.filter(
            access_level="public",
            is_published=True
        ).count(),
    }
    return render(request, "public_portal/home.html", context)


def public_bills(request):
    query = request.GET.get("q", "").strip()

    bills = Bill.objects.filter(is_public=True).select_related("sponsor")

    if query:
        bills = bills.filter(
            Q(title__icontains=query) |
            Q(bill_number__icontains=query) |
            Q(summary__icontains=query) |
            Q(sponsor__first_name__icontains=query) |
            Q(sponsor__last_name__icontains=query)
        )

    return render(request, "public_portal/public_bills.html", {
        "page_title": "Published Bills",
        "bills": bills,
        "query": query,
    })


def public_motions(request):
    query = request.GET.get("q", "").strip()

    motions = Motion.objects.filter(is_public=True).select_related("sponsor")

    if query:
        motions = motions.filter(
            Q(title__icontains=query) |
            Q(motion_number__icontains=query) |
            Q(description__icontains=query) |
            Q(sponsor__first_name__icontains=query) |
            Q(sponsor__last_name__icontains=query)
        )

    return render(request, "public_portal/public_motions.html", {
        "page_title": "Published Motions",
        "motions": motions,
        "query": query,
    })


def public_resolutions(request):
    query = request.GET.get("q", "").strip()

    resolutions = Resolution.objects.filter(is_public=True).select_related("related_motion")

    if query:
        resolutions = resolutions.filter(
            Q(title__icontains=query) |
            Q(resolution_number__icontains=query) |
            Q(description__icontains=query) |
            Q(decision_summary__icontains=query)
        )

    return render(request, "public_portal/public_resolutions.html", {
        "page_title": "Published Resolutions",
        "resolutions": resolutions,
        "query": query,
    })


def public_sittings(request):
    query = request.GET.get("q", "").strip()

    sittings = PlenarySitting.objects.filter(is_public=True)

    if query:
        sittings = sittings.filter(
            Q(title__icontains=query) |
            Q(sitting_number__icontains=query) |
            Q(venue__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, "public_portal/public_sittings.html", {
        "page_title": "Published Sittings",
        "sittings": sittings,
        "query": query,
    })


def public_documents(request):
    query = request.GET.get("q", "").strip()

    documents = DocumentFile.objects.filter(
        access_level="public",
        is_published=True
    ).select_related("category")

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, "public_portal/public_documents.html", {
        "page_title": "Public Documents",
        "documents": documents,
        "query": query,
    })


def public_search(request):
    query = request.GET.get("q", "").strip()

    bills = motions = resolutions = sittings = documents = []

    if query:
        bills = Bill.objects.filter(is_public=True).filter(
            Q(title__icontains=query) |
            Q(bill_number__icontains=query) |
            Q(summary__icontains=query)
        )[:10]

        motions = Motion.objects.filter(is_public=True).filter(
            Q(title__icontains=query) |
            Q(motion_number__icontains=query) |
            Q(description__icontains=query)
        )[:10]

        resolutions = Resolution.objects.filter(is_public=True).filter(
            Q(title__icontains=query) |
            Q(resolution_number__icontains=query) |
            Q(description__icontains=query)
        )[:10]

        sittings = PlenarySitting.objects.filter(is_public=True).filter(
            Q(title__icontains=query) |
            Q(sitting_number__icontains=query) |
            Q(description__icontains=query)
        )[:10]

        documents = DocumentFile.objects.filter(
            access_level="public",
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:10]

    return render(request, "public_portal/public_search.html", {
        "page_title": "Public Search",
        "query": query,
        "bills": bills,
        "motions": motions,
        "resolutions": resolutions,
        "sittings": sittings,
        "documents": documents,
    })