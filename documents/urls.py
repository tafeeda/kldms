from django.urls import path

from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("upload/", views.document_create, name="document_create"),
    path("<int:pk>/", views.document_detail, name="document_detail"),
    path("<int:pk>/edit/", views.document_update, name="document_update"),
    path("<int:pk>/download/", views.document_download, name="document_download"),
    path("<int:pk>/toggle-publish/", views.document_toggle_publish, name="document_toggle_publish"),
    path("<int:document_id>/versions/add/", views.document_add_version, name="document_add_version"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
]