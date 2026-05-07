from django.urls import path
from . import views

urlpatterns = [
    path("", views.public_home, name="public_home"),
    path("public/bills/", views.public_bills, name="public_bills"),
    path("public/motions/", views.public_motions, name="public_motions"),
    path("public/resolutions/", views.public_resolutions, name="public_resolutions"),
    path("public/sittings/", views.public_sittings, name="public_sittings"),
    path("public/documents/", views.public_documents, name="public_documents"),
    path("public/search/", views.public_search, name="public_search"),
]