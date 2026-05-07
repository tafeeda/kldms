from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from audit.models import AuditLog
from audit.utils import log_audit

from django.utils import timezone

from .models import FailedLoginAttempt
from audit.utils import get_client_ip




from .decorators import super_admin_required
from .forms import (
    MyProfileUpdateForm,
    MyUserUpdateForm,
    SecurePasswordChangeForm,
    UserCreateForm,
    UserUpdateForm,
)
from .models import UserProfile


@super_admin_required
def user_list(request):
    users = User.objects.select_related("profile").order_by("username")

    context = {
        "page_title": "User Management",
        "users": users,
    }
    return render(request, "accounts/user_list.html", context)


@super_admin_required
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = form.cleaned_data["role"]
            profile.official_title = form.cleaned_data["official_title"]
            profile.phone = form.cleaned_data["phone"]
            profile.save()

            log_audit(
                request,
                AuditLog.ACTION_CREATE,
                "Accounts",
                f"Created user account: {user.username}",
                user
            )

            messages.success(request, "User account created successfully.")
            return redirect("user_list")
    else:
        form = UserCreateForm()

    return render(request, "accounts/user_form.html", {
        "page_title": "Create User",
        "form": form,
        "form_title": "Create User Account",
    })


@super_admin_required
def user_update(request, pk):
    user = get_object_or_404(User.objects.select_related("profile"), pk=pk)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save()

            profile.role = form.cleaned_data["role"]
            profile.official_title = form.cleaned_data["official_title"]
            profile.phone = form.cleaned_data["phone"]

            if form.cleaned_data.get("profile_photo"):
                profile.profile_photo = form.cleaned_data["profile_photo"]

            profile.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Accounts",
                f"Updated user account: {user.username}",
                user
            )

            messages.success(request, "User account updated successfully.")
            return redirect("user_list")
    else:
        form = UserUpdateForm(instance=user, initial={
            "role": profile.role,
            "official_title": profile.official_title,
            "phone": profile.phone,
        })

    return render(request, "accounts/user_form.html", {
        "page_title": "Update User",
        "form": form,
        "form_title": "Update User Account",
    })


@super_admin_required
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("user_list")

    user.is_active = not user.is_active
    user.save()

    log_audit(
        request,
        AuditLog.ACTION_UPDATE,
        "Accounts",
        f"Toggled active status for user: {user.username}",
        user
    )

    messages.success(request, "User status updated successfully.")
    return redirect("user_list")


@login_required
def my_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = MyUserUpdateForm(request.POST, instance=request.user)
        profile_form = MyProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Accounts",
                "Updated own profile.",
                request.user
            )

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("my_profile")
    else:
        user_form = MyUserUpdateForm(instance=request.user)
        profile_form = MyProfileUpdateForm(instance=profile)

    return render(request, "accounts/my_profile.html", {
        "page_title": "My Profile",
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def change_my_password(request):
    if request.method == "POST":
        form = SecurePasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            log_audit(
                request,
                AuditLog.ACTION_UPDATE,
                "Accounts",
                "Changed own password.",
                request.user
            )

            messages.success(request, "Password changed successfully.")
            return redirect("my_profile")
    else:
        form = SecurePasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {
        "page_title": "Change Password",
        "form": form,
    })




def custom_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        ip = get_client_ip(request)

        record = FailedLoginAttempt.objects.filter(
            username=username,
            ip_address=ip
        ).first()

        # 🔒 Check if locked
        if record and record.is_locked:
            if record.locked_until and record.locked_until > timezone.now():
                messages.error(
                    request,
                    "Too many failed attempts. Try again later."
                )
                return redirect("login")
            else:
                # Auto unlock
                record.is_locked = False
                record.attempt_count = 0
                record.save()

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")