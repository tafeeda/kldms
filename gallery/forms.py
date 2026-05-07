from django import forms

from .models import OfficialProfile


class OfficialProfileForm(forms.ModelForm):
    class Meta:
        model = OfficialProfile
        fields = [
            "full_name",
            "position_title",
            "category",
            "photo",
            "constituency",
            "political_party",
            "short_biography",
            "start_date",
            "end_date",
            "status",
            "display_order",
            "is_published",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "position_title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "constituency": forms.Select(attrs={"class": "form-control"}),
            "political_party": forms.Select(attrs={"class": "form-control"}),
            "short_biography": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "display_order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }