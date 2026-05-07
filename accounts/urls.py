from django.contrib.auth import views as auth_views
from django_ratelimit.decorators import ratelimit
from django.urls import path
from . import views

urlpatterns = [
    path(
        "login/",
        ratelimit(key="ip", rate="5/m", method="POST", block=True)(
            views.custom_login
        ),
        name="login"
    ),
    
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:pk>/edit/", views.user_update, name="user_update"),
    path("users/<int:pk>/toggle-active/", views.user_toggle_active, name="user_toggle_active"),

    path("profile/", views.my_profile, name="my_profile"),
    path("profile/change-password/", views.change_my_password, name="change_my_password"),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/reset/done/",
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]

