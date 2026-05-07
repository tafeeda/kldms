from django import forms
from django.contrib.auth.models import User

from accounts.models import UserProfile
from .models import Committee, CommitteeDocument, CommitteeMembership


class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = [
            "name",
            "committee_type",
            "description",
            "chairman",
            "vice_chairman",
            "committee_clerk",
            "is_active",
            "display_order",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "committee_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "chairman": forms.Select(attrs={"class": "form-control"}),
            "vice_chairman": forms.Select(attrs={"class": "form-control"}),
            "committee_clerk": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "display_order": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["committee_clerk"].queryset = User.objects.filter(
            profile__role__in=[
                UserProfile.ROLE_SUPER_ADMIN,
                UserProfile.ROLE_CLERK,
                UserProfile.ROLE_DEPUTY_CLERK,
                UserProfile.ROLE_COMMITTEE_CLERK,
            ],
            is_active=True
        ).order_by("username")


class CommitteeMembershipForm(forms.ModelForm):
    class Meta:
        model = CommitteeMembership
        fields = [
            "member",
            "role",
            "date_joined",
            "is_active",
        ]

        widgets = {
            "member": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "date_joined": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommitteeDocumentForm(forms.ModelForm):
    class Meta:
        model = CommitteeDocument
        fields = [
            "title",
            "description",
            "file",
            "access_level",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "access_level": forms.Select(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }