from django.urls import path

from . import views

urlpatterns = [
    path("parties/", views.party_list, name="party_list"),
    path("parties/create/", views.party_create, name="party_create"),
    path("parties/<int:pk>/edit/", views.party_update, name="party_update"),

    path("", views.constituency_list, name="constituency_list"),
    path("create/", views.constituency_create, name="constituency_create"),
    path("<int:pk>/edit/", views.constituency_update, name="constituency_update"),
]