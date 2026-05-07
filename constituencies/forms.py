from django import forms

from .models import Constituency, PoliticalParty


class PoliticalPartyForm(forms.ModelForm):
    class Meta:
        model = PoliticalParty
        fields = [
            "name",
            "abbreviation",
            "logo",
            "description",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "abbreviation": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ConstituencyForm(forms.ModelForm):
    class Meta:
        model = Constituency
        fields = [
            "name",
            "local_government",
            "description",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "local_government": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }