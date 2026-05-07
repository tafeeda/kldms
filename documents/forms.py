from django import forms

from .models import DocumentCategory, DocumentFile, DocumentVersion


class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ["name", "description", "is_active"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class DocumentFileForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = [
            "title",
            "category",
            "description",
            "file",
            "access_level",
            "is_published",
            "version_number",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "access_level": forms.Select(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "version_number": forms.NumberInput(attrs={"class": "form-control"}),
        }


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        model = DocumentVersion
        fields = ["version_number", "file", "notes"]

        widgets = {
            "version_number": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }