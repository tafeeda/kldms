from django.urls import path

from . import views

urlpatterns = [
    path("", views.sitting_list, name="sitting_list"),
    path("create/", views.sitting_create, name="sitting_create"),
    path("<int:pk>/", views.sitting_detail, name="sitting_detail"),
    path("<int:pk>/edit/", views.sitting_update, name="sitting_update"),
    path("<int:pk>/toggle-public/", views.sitting_toggle_public, name="sitting_toggle_public"),

    path("<int:sitting_id>/agenda/add/", views.agenda_add, name="agenda_add"),
    path("agenda/<int:pk>/edit/", views.agenda_update, name="agenda_update"),

    path("<int:sitting_id>/order-paper/", views.order_paper_manage, name="order_paper_manage"),
    path("<int:sitting_id>/votes-proceeding/", views.votes_proceeding_manage, name="votes_proceeding_manage"),
    path("<int:sitting_id>/hansard/", views.hansard_manage, name="hansard_manage"),

    path("<int:sitting_id>/documents/upload/", views.sitting_upload_document, name="sitting_upload_document"),
    path("documents/<int:pk>/toggle-public/", views.sitting_toggle_document_public, name="sitting_toggle_document_public"),
]