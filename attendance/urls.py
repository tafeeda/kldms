from django.urls import path

from . import views

urlpatterns = [
    path("", views.attendance_session_list, name="attendance_session_list"),
    path("create/", views.attendance_session_create, name="attendance_session_create"),
    path("reports/", views.attendance_report, name="attendance_report"),

    path("<int:pk>/", views.attendance_session_detail, name="attendance_session_detail"),
    path("<int:pk>/edit/", views.attendance_session_update, name="attendance_session_update"),
    path("<int:pk>/toggle-lock/", views.attendance_toggle_lock, name="attendance_toggle_lock"),

    path("<int:session_id>/records/add/", views.attendance_add_record, name="attendance_add_record"),
    path("records/<int:pk>/edit/", views.attendance_update_record, name="attendance_update_record"),
    path("<int:session_id>/bulk-mark/", views.attendance_bulk_mark, name="attendance_bulk_mark"),
]