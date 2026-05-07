from django.db import models


class SystemSetting(models.Model):
    institution_name = models.CharField(
        max_length=255,
        default="Kano State House of Assembly"
    )
    system_name = models.CharField(
        max_length=255,
        default="Kano Legislative Digital Management System"
    )
    short_name = models.CharField(max_length=50, default="KLDMS")

    logo = models.ImageField(upload_to="system/", blank=True, null=True)
    favicon = models.ImageField(upload_to="system/", blank=True, null=True)

    primary_color = models.CharField(max_length=20, default="#0B6B3A")
    secondary_color = models.CharField(max_length=20, default="#FFFFFF")
    accent_color = models.CharField(max_length=20, default="#111827")

    public_hero_title = models.CharField(
        max_length=255,
        default="Kano State House of Assembly Public Transparency Portal"
    )
    public_hero_subtitle = models.TextField(
        default="Access published legislative information, bills, motions, resolutions, sittings, documents, and official public records."
    )

    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    footer_text = models.CharField(
        max_length=255,
        default="Kano Legislative Digital Management System. All rights reserved."
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return self.system_name

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj