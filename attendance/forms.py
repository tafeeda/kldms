from django import forms

from .models import AttendanceRecord, AttendanceSession


class AttendanceSessionForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = [
            "title",
            "attendance_type",
            "sitting",
            "committee",
            "attendance_date",
            "description",
            "is_locked",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "attendance_type": forms.Select(attrs={"class": "form-control"}),
            "sitting": forms.Select(attrs={"class": "form-control"}),
            "committee": forms.Select(attrs={"class": "form-control"}),
            "attendance_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_locked": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ["member", "status", "remarks"]

        widgets = {
            "member": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }


class AttendanceBulkRecordForm(forms.Form):
    def __init__(self, *args, members=None, **kwargs):
        super().__init__(*args, **kwargs)

        if members:
            for member in members:
                self.fields[f"member_{member.id}"] = forms.ChoiceField(
                    label=str(member),
                    choices=AttendanceRecord.STATUS_CHOICES,
                    initial=AttendanceRecord.STATUS_ABSENT,
                    widget=forms.Select(attrs={"class": "form-control"})
                )

                self.fields[f"remarks_{member.id}"] = forms.CharField(
                    required=False,
                    label="Remarks",
                    widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional remarks"})
                )