from django.urls import path

from . import views

urlpatterns = [
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/create/", views.bill_create, name="bill_create"),
    path("bills/<int:pk>/", views.bill_detail, name="bill_detail"),
    path("bills/<int:pk>/edit/", views.bill_update, name="bill_update"),
    path("bills/<int:pk>/toggle-public/", views.bill_toggle_public, name="bill_toggle_public"),

    path("bills/<int:bill_id>/readings/add/", views.bill_add_reading, name="bill_add_reading"),

    path("bills/<int:bill_id>/amendments/add/", views.bill_add_amendment, name="bill_add_amendment"),
    path("bills/amendments/<int:pk>/edit/", views.bill_update_amendment, name="bill_update_amendment"),

    path("bills/<int:bill_id>/documents/upload/", views.bill_upload_document, name="bill_upload_document"),
    path("bills/documents/<int:pk>/toggle-public/", views.bill_toggle_document_public, name="bill_toggle_document_public"),


    path("motions/", views.motion_list, name="motion_list"),
    path("motions/create/", views.motion_create, name="motion_create"),
    path("motions/<int:pk>/", views.motion_detail, name="motion_detail"),
    path("motions/<int:pk>/edit/", views.motion_update, name="motion_update"),
    path("motions/<int:pk>/toggle-public/", views.motion_toggle_public, name="motion_toggle_public"),
    path("motions/<int:motion_id>/documents/upload/", views.motion_upload_document, name="motion_upload_document"),
    path("motions/documents/<int:pk>/toggle-public/", views.motion_toggle_document_public, name="motion_toggle_document_public"),

    path("resolutions/", views.resolution_list, name="resolution_list"),
    path("resolutions/create/", views.resolution_create, name="resolution_create"),
    path("resolutions/<int:pk>/", views.resolution_detail, name="resolution_detail"),
    path("resolutions/<int:pk>/edit/", views.resolution_update, name="resolution_update"),
    path("resolutions/<int:pk>/toggle-public/", views.resolution_toggle_public, name="resolution_toggle_public"),
    path("resolutions/<int:resolution_id>/documents/upload/", views.resolution_upload_document, name="resolution_upload_document"),
    path("resolutions/documents/<int:pk>/toggle-public/", views.resolution_toggle_document_public, name="resolution_toggle_document_public"),
]