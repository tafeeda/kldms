from django.urls import path

from . import views

urlpatterns = [
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("print/", views.printable_report, name="printable_report"),
]