from django import forms

from .models import HonourableMember


class HonourableMemberForm(forms.ModelForm):
    class Meta:
        model = HonourableMember
        fields = [
            "user_account",
            "title",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone",
            "email",
            "photo",
            "constituency",
            "political_party",
            "position_title",
            "biography",
            "date_sworn_in",
            "end_date",
            "status",
            "display_order",
            "is_published",
        ]

        widgets = {
            "user_account": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "constituency": forms.Select(attrs={"class": "form-control"}),
            "political_party": forms.Select(attrs={"class": "form-control"}),
            "position_title": forms.TextInput(attrs={"class": "form-control"}),
            "biography": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "date_sworn_in": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "display_order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }