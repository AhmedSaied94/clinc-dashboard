"""
Forms for dashboard app.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from placements.models import Placement
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class PlacementForm(forms.ModelForm):
    """Form for creating and editing placements."""

    class Meta:
        model = Placement
        fields = [
            "date",
            "shift",
            "physician_name",
            "physician_id",
            "department",
            "specialty",
            "status",
            "area",
            "room_number",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "shift": forms.Select(attrs={"class": "form-select"}),
            "physician_name": forms.TextInput(attrs={"class": "form-control"}),
            "physician_id": forms.NumberInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "specialty": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "area": forms.TextInput(attrs={"class": "form-control"}),
            "room_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("physician_name", css_class="col-md-6"),
                Column("physician_id", css_class="col-md-6"),
            ),
            Row(
                Column("date", css_class="col-md-4"),
                Column("shift", css_class="col-md-4"),
                Column("status", css_class="col-md-4"),
            ),
            Row(
                Column("department", css_class="col-md-6"),
                Column("specialty", css_class="col-md-6"),
            ),
            Row(
                Column("area", css_class="col-md-6"),
                Column("room_number", css_class="col-md-6"),
            ),
            Submit("submit", "Save Placement", css_class="btn btn-primary mt-3"),
        )


class FilterForm(forms.Form):
    """Form for filtering analytics data."""

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    department = forms.ChoiceField(
        required=False, widget=forms.Select(attrs={"class": "form-select"})
    )
    specialty = forms.ChoiceField(
        required=False, widget=forms.Select(attrs={"class": "form-select"})
    )
    shift = forms.ChoiceField(
        required=False,
        choices=[("", "All Shifts")] + list(Placement.SHIFT_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All Statuses")] + list(Placement.STATUS_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        exclude_field = kwargs.pop("exclude_field", None)
        super().__init__(*args, **kwargs)

        # Remove excluded field if specified
        if exclude_field and exclude_field in self.fields:
            del self.fields[exclude_field]

        # Populate department choices dynamically
        if "department" in self.fields:
            departments = (
                Placement.objects.values_list("department", flat=True)
                .distinct()
                .order_by("department")
            )
            self.fields["department"].choices = [("", "All Departments")] + [
                (d, d) for d in departments if d
            ]

        # Populate specialty choices dynamically
        if "specialty" in self.fields:
            specialties = (
                Placement.objects.values_list("specialty", flat=True)
                .distinct()
                .order_by("specialty")
            )
            self.fields["specialty"].choices = [("", "All Specialties")] + [
                (s, s) for s in specialties if s
            ]


class UserForm(forms.ModelForm):
    """Form for creating and editing users."""

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Leave blank to keep the current password.",
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Confirm the password.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Editing existing user - password not required
            self.fields["password"].required = False
            self.fields["confirm_password"].required = False
        else:
            # Creating new user - password required
            self.fields["password"].required = True
            self.fields["confirm_password"].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # If creating new user or password is provided, validate it
        if not self.instance.pk or password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
            if password and len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class ImportPlacementsForm(forms.Form):
    """Form for importing placements from Excel file."""

    excel_file = forms.FileField(
        label="Excel File",
        help_text="Upload an Excel file (.xlsx) with placement data",
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "accept": ".xlsx,.xls",
        }),
    )
    replace = forms.BooleanField(
        required=False,
        initial=False,
        label="Replace existing data",
        help_text="If checked, all existing placements will be deleted before importing new data",
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
        }),
    )


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class SettingsForm(forms.Form):
    """Form for application settings."""

    theme = forms.ChoiceField(
        choices=[("light", "Light"), ("dark", "Dark"), ("auto", "Auto")],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Theme Preference",
    )
    notifications = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Enable Notifications",
    )
    email_notifications = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Email Notifications",
    )
