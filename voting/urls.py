from django.urls import path

from . import views

urlpatterns = [
    path("", views.vote_session_list, name="vote_session_list"),
    path("create/", views.vote_session_create, name="vote_session_create"),
    path("reports/", views.vote_report, name="vote_report"),

    path("<int:pk>/", views.vote_session_detail, name="vote_session_detail"),
    path("<int:pk>/edit/", views.vote_session_update, name="vote_session_update"),
    path("<int:pk>/toggle-lock/", views.vote_session_toggle_lock, name="vote_session_toggle_lock"),
    path("<int:pk>/toggle-open/", views.vote_session_toggle_open, name="vote_session_toggle_open"),
    path("<int:pk>/toggle-public/", views.vote_session_toggle_public, name="vote_session_toggle_public"),
    path("<int:pk>/compute-outcome/", views.vote_compute_outcome, name="vote_compute_outcome"),

    path("<int:session_id>/records/add/", views.vote_add_record, name="vote_add_record"),
    path("records/<int:pk>/edit/", views.vote_update_record, name="vote_update_record"),
    path("<int:session_id>/bulk-mark/", views.vote_bulk_mark, name="vote_bulk_mark"),
]