from django import forms

from .models import SystemSetting


class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = [
            "institution_name",
            "system_name",
            "short_name",
            "logo",
            "favicon",
            "primary_color",
            "secondary_color",
            "accent_color",
            "public_hero_title",
            "public_hero_subtitle",
            "address",
            "phone",
            "email",
            "website",
            "footer_text",
        ]

        widgets = {
            "institution_name": forms.TextInput(attrs={"class": "form-control"}),
            "system_name": forms.TextInput(attrs={"class": "form-control"}),
            "short_name": forms.TextInput(attrs={"class": "form-control"}),
            "primary_color": forms.TextInput(attrs={"class": "form-control", "type": "color"}),
            "secondary_color": forms.TextInput(attrs={"class": "form-control", "type": "color"}),
            "accent_color": forms.TextInput(attrs={"class": "form-control", "type": "color"}),
            "public_hero_title": forms.TextInput(attrs={"class": "form-control"}),
            "public_hero_subtitle": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "footer_text": forms.TextInput(attrs={"class": "form-control"}),
        }