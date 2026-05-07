from django.urls import path

from . import views

urlpatterns = [
    path("live/", views.live_master_search, name="live_master_search"),
]