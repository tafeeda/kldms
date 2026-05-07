from django.urls import path

from . import views

urlpatterns = [
    path("public/officials/", views.public_official_gallery, name="public_official_gallery"),

    path("", views.official_list, name="official_list"),
    path("create/", views.official_create, name="official_create"),
    path("<int:pk>/", views.official_detail, name="official_detail"),
    path("<int:pk>/edit/", views.official_update, name="official_update"),
    path("<int:pk>/toggle-publish/", views.official_toggle_publish, name="official_toggle_publish"),
]