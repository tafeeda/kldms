from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import ConstituencyForm, PoliticalPartyForm
from .models import Constituency, PoliticalParty


@clerk_or_admin_required
def party_list(request):
    parties = PoliticalParty.objects.all()

    return render(request, "constituencies/party_list.html", {
        "page_title": "Political Parties",
        "parties": parties,
    })


@clerk_or_admin_required
def party_create(request):
    if request.method == "POST":
        form = PoliticalPartyForm(request.POST, request.FILES)

        if form.is_valid():
            party = form.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Political Parties",
                f"Created political party: {party}",
                party
            )

            messages.success(request, "Political party created successfully.")
            return redirect("party_list")
    else:
        form = PoliticalPartyForm()

    return render(request, "constituencies/party_form.html", {
        "page_title": "Create Political Party",
        "form": form,
        "form_title": "Create Political Party",
    })


@clerk_or_admin_required
def party_update(request, pk):
    party = get_object_or_404(PoliticalParty, pk=pk)

    if request.method == "POST":
        form = PoliticalPartyForm(request.POST, request.FILES, instance=party)

        if form.is_valid():
            party = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Political Parties",
                f"Updated political party: {party}",
                party
            )

            messages.success(request, "Political party updated successfully.")
            return redirect("party_list")
    else:
        form = PoliticalPartyForm(instance=party)

    return render(request, "constituencies/party_form.html", {
        "page_title": "Update Political Party",
        "form": form,
        "form_title": "Update Political Party",
    })


@clerk_or_admin_required
def constituency_list(request):
    constituencies = Constituency.objects.all()

    return render(request, "constituencies/constituency_list.html", {
        "page_title": "Constituencies",
        "constituencies": constituencies,
    })


@clerk_or_admin_required
def constituency_create(request):
    if request.method == "POST":
        form = ConstituencyForm(request.POST)

        if form.is_valid():
            constituency = form.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Constituencies",
                f"Created constituency: {constituency}",
                constituency
            )

            messages.success(request, "Constituency created successfully.")
            return redirect("constituency_list")
    else:
        form = ConstituencyForm()

    return render(request, "constituencies/constituency_form.html", {
        "page_title": "Create Constituency",
        "form": form,
        "form_title": "Create Constituency",
    })


@clerk_or_admin_required
def constituency_update(request, pk):
    constituency = get_object_or_404(Constituency, pk=pk)

    if request.method == "POST":
        form = ConstituencyForm(request.POST, instance=constituency)

        if form.is_valid():
            constituency = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Constituencies",
                f"Updated constituency: {constituency}",
                constituency
            )

            messages.success(request, "Constituency updated successfully.")
            return redirect("constituency_list")
    else:
        form = ConstituencyForm(instance=constituency)

    return render(request, "constituencies/constituency_form.html", {
        "page_title": "Update Constituency",
        "form": form,
        "form_title": "Update Constituency",
    })