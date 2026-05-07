from django.contrib import admin

from .models import Constituency, PoliticalParty


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "abbreviation"]


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ["name", "local_government", "is_active", "created_at"]
    list_filter = ["is_active", "local_government", "created_at"]
    search_fields = ["name", "local_government"]