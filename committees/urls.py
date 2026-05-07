from django.urls import path

from . import views

urlpatterns = [
    path("", views.committee_list, name="committee_list"),
    path("create/", views.committee_create, name="committee_create"),
    path("<int:pk>/", views.committee_detail, name="committee_detail"),
    path("<int:pk>/edit/", views.committee_update, name="committee_update"),

    path("<int:committee_id>/members/add/", views.committee_add_member, name="committee_add_member"),
    path("members/<int:pk>/edit/", views.committee_update_member, name="committee_update_member"),
    path("members/<int:pk>/remove/", views.committee_remove_member, name="committee_remove_member"),

    path("<int:committee_id>/documents/upload/", views.committee_upload_document, name="committee_upload_document"),
    path("documents/<int:pk>/toggle-publish/", views.committee_toggle_document_publish, name="committee_toggle_document_publish"),
]