from django import forms

from .models import VoteRecord, VoteSession


class VoteSessionForm(forms.ModelForm):
    class Meta:
        model = VoteSession
        fields = [
            "title",
            "vote_number",
            "vote_type",
            "vote_method",
            "sitting",
            "bill",
            "motion",
            "resolution",
            "description",
            "outcome",
            "decision_summary",
            "vote_date",
            "is_open",
            "is_locked",
            "is_public",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "vote_number": forms.TextInput(attrs={"class": "form-control"}),
            "vote_type": forms.Select(attrs={"class": "form-control"}),
            "vote_method": forms.Select(attrs={"class": "form-control"}),
            "sitting": forms.Select(attrs={"class": "form-control"}),
            "bill": forms.Select(attrs={"class": "form-control"}),
            "motion": forms.Select(attrs={"class": "form-control"}),
            "resolution": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "outcome": forms.Select(attrs={"class": "form-control"}),
            "decision_summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "vote_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_open": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_locked": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class VoteRecordForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
        fields = ["member", "choice", "remarks"]

        widgets = {
            "member": forms.Select(attrs={"class": "form-control"}),
            "choice": forms.Select(attrs={"class": "form-control"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }


class BulkVoteForm(forms.Form):
    def __init__(self, *args, members=None, **kwargs):
        super().__init__(*args, **kwargs)

        if members:
            for member in members:
                self.fields[f"member_{member.id}"] = forms.ChoiceField(
                    label=str(member),
                    choices=VoteRecord.CHOICE_CHOICES,
                    initial=VoteRecord.CHOICE_ABSTAIN,
                    widget=forms.Select(attrs={"class": "form-control"})
                )

                self.fields[f"remarks_{member.id}"] = forms.CharField(
                    required=False,
                    label=f"Remarks for {member}",
                    widget=forms.TextInput(
                        attrs={
                            "class": "form-control",
                            "placeholder": "Optional remarks"
                        }
                    )
                )