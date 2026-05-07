from django import forms

from .models import (
    HansardTranscript,
    OrderPaper,
    PlenarySitting,
    SittingAgendaItem,
    SittingDocument,
    VotesProceeding,
)


class PlenarySittingForm(forms.ModelForm):
    class Meta:
        model = PlenarySitting
        fields = [
            "title",
            "sitting_number",
            "sitting_date",
            "start_time",
            "end_time",
            "venue",
            "status",
            "description",
            "is_public",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "sitting_number": forms.TextInput(attrs={"class": "form-control"}),
            "sitting_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "venue": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SittingAgendaItemForm(forms.ModelForm):
    class Meta:
        model = SittingAgendaItem
        fields = [
            "title",
            "description",
            "order_number",
            "presenter",
            "is_completed",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "order_number": forms.NumberInput(attrs={"class": "form-control"}),
            "presenter": forms.TextInput(attrs={"class": "form-control"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class OrderPaperForm(forms.ModelForm):
    class Meta:
        model = OrderPaper
        fields = ["title", "content", "file", "is_published"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class VotesProceedingForm(forms.ModelForm):
    class Meta:
        model = VotesProceeding
        fields = ["title", "content", "file", "is_published"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class HansardTranscriptForm(forms.ModelForm):
    class Meta:
        model = HansardTranscript
        fields = ["title", "transcript", "file", "is_published"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "transcript": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SittingDocumentForm(forms.ModelForm):
    class Meta:
        model = SittingDocument
        fields = ["title", "description", "file", "is_public"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }