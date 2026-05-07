from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import clerk_or_admin_required, legislative_staff_required
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import HonourableMemberForm
from .models import HonourableMember


@legislative_staff_required
def member_list(request):
    query = request.GET.get("q", "").strip()

    members = HonourableMember.objects.select_related(
        "constituency",
        "political_party",
        "user_account",
    )

    if query:
        members = members.filter(
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(position_title__icontains=query) |
            Q(constituency__name__icontains=query) |
            Q(political_party__name__icontains=query) |
            Q(political_party__abbreviation__icontains=query)
        )

    return render(request, "members/member_list.html", {
        "page_title": "Honourable Members",
        "members": members,
        "query": query,
    })


@legislative_staff_required
def member_detail(request, pk):
    member = get_object_or_404(
        HonourableMember.objects.select_related(
            "constituency",
            "political_party",
            "user_account",
        ),
        pk=pk
    )

    log_audit(
        request,
        AuditLog.ACTION_VIEW,
        "Honourable Members",
        f"Viewed member profile: {member}",
        member
    )

    return render(request, "members/member_detail.html", {
        "page_title": member.full_name,
        "member": member,
    })


@clerk_or_admin_required
def member_create(request):
    if request.method == "POST":
        form = HonourableMemberForm(request.POST, request.FILES)

        if form.is_valid():
            member = form.save(commit=False)
            member.created_by = request.user
            member.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Honourable Members",
                f"Created member profile: {member}",
                member
            )

            messages.success(request, "Honourable member profile created successfully.")
            return redirect("member_detail", pk=member.pk)
    else:
        form = HonourableMemberForm()

    return render(request, "members/member_form.html", {
        "page_title": "Create Honourable Member",
        "form": form,
        "form_title": "Create Honourable Member",
    })


@clerk_or_admin_required
def member_update(request, pk):
    member = get_object_or_404(HonourableMember, pk=pk)

    if request.method == "POST":
        form = HonourableMemberForm(request.POST, request.FILES, instance=member)

        if form.is_valid():
            member = form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Honourable Members",
                f"Updated member profile: {member}",
                member
            )

            messages.success(request, "Honourable member profile updated successfully.")
            return redirect("member_detail", pk=member.pk)
    else:
        form = HonourableMemberForm(instance=member)

    return render(request, "members/member_form.html", {
        "page_title": "Update Honourable Member",
        "form": form,
        "form_title": "Update Honourable Member",
    })


@clerk_or_admin_required
def member_toggle_publish(request, pk):
    member = get_object_or_404(HonourableMember, pk=pk)
    member.is_published = not member.is_published
    member.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Honourable Members",
        f"Toggled publish status for member: {member}",
        member
    )

    messages.success(request, "Member publish status updated successfully.")
    return redirect("member_detail", pk=member.pk)