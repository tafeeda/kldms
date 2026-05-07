from django.db import models


class PoliticalParty(models.Model):
    name = models.CharField(max_length=150, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)
    logo = models.ImageField(upload_to="party_logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Political Parties"

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Constituency(models.Model):
    name = models.CharField(max_length=150, unique=True)
    local_government = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Constituencies"

    def __str__(self):
        return self.name