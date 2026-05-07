from django import forms
from .models import (
    Bill,
    BillAmendment,
    BillDocument,
    BillReading,
    Motion,
    MotionDocument,
    Resolution,
    ResolutionDocument,
)


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            "title",
            "bill_number",
            "summary",
            "long_title",
            "sponsor",
            "co_sponsors",
            "status",
            "date_introduced",
            "date_passed",
            "date_assented",
            "is_public",
            "is_archived",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "bill_number": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "long_title": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "sponsor": forms.Select(attrs={"class": "form-control"}),
            "co_sponsors": forms.SelectMultiple(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "date_introduced": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "date_passed": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "date_assented": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_archived": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BillReadingForm(forms.ModelForm):
    class Meta:
        model = BillReading
        fields = ["reading_type", "reading_date", "notes"]

        widgets = {
            "reading_type": forms.Select(attrs={"class": "form-control"}),
            "reading_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class BillAmendmentForm(forms.ModelForm):
    class Meta:
        model = BillAmendment
        fields = [
            "title",
            "description",
            "proposed_by",
            "amendment_date",
            "is_approved",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "proposed_by": forms.Select(attrs={"class": "form-control"}),
            "amendment_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BillDocumentForm(forms.ModelForm):
    class Meta:
        model = BillDocument
        fields = [
            "title",
            "file",
            "description",
            "is_public",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }



class MotionForm(forms.ModelForm):
    class Meta:
        model = Motion
        fields = [
            "title",
            "motion_number",
            "description",
            "sponsor",
            "co_sponsors",
            "status",
            "decision",
            "date_moved",
            "date_decided",
            "is_public",
            "is_archived",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "motion_number": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "sponsor": forms.Select(attrs={"class": "form-control"}),
            "co_sponsors": forms.SelectMultiple(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "decision": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date_moved": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "date_decided": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_archived": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MotionDocumentForm(forms.ModelForm):
    class Meta:
        model = MotionDocument
        fields = ["title", "file", "description", "is_public"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = [
            "title",
            "resolution_number",
            "description",
            "related_motion",
            "status",
            "decision_summary",
            "date_adopted",
            "is_public",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "resolution_number": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "related_motion": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "decision_summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date_adopted": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ResolutionDocumentForm(forms.ModelForm):
    class Meta:
        model = ResolutionDocument
        fields = ["title", "file", "description", "is_public"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }