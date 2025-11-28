"""
Dashboard views for clinic placement management and analytics.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
    FormView,
    View,
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required as login_required_decorator
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from placements.models import Placement
from .forms import (
    PlacementForm,
    FilterForm,
    UserForm,
    ImportPlacementsForm,
    ProfileForm,
    SettingsForm,
)
from datetime import datetime, timedelta
import pandas as pd
import logging
import tempfile
import os
from io import BytesIO

logger = logging.getLogger(__name__)


class LoginView(BaseLoginView):
    """Custom login view with modern design."""

    template_name = "dashboard/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.success(
            self.request,
            f"Welcome back, {form.get_user().get_full_name() or form.get_user().username}!",
        )
        return redirect(self.get_success_url())


@require_POST
@login_required_decorator
def logout_view(request):
    """Custom logout view."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("dashboard:login")


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main analytics dashboard view."""

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters
        filter_form = FilterForm(self.request.GET or None)
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters if form is valid
        if filter_form.is_valid():
            if filter_form.cleaned_data.get("start_date"):
                queryset = queryset.filter(
                    date__gte=filter_form.cleaned_data["start_date"]
                )
            if filter_form.cleaned_data.get("end_date"):
                queryset = queryset.filter(
                    date__lte=filter_form.cleaned_data["end_date"]
                )
            if filter_form.cleaned_data.get("department"):
                queryset = queryset.filter(
                    department=filter_form.cleaned_data["department"]
                )
            if filter_form.cleaned_data.get("specialty"):
                queryset = queryset.filter(
                    specialty=filter_form.cleaned_data["specialty"]
                )
            if filter_form.cleaned_data.get("shift"):
                queryset = queryset.filter(shift=filter_form.cleaned_data["shift"])
            if filter_form.cleaned_data.get("status"):
                queryset = queryset.filter(status=filter_form.cleaned_data["status"])

        # Statistics
        context["total_placements"] = queryset.count()
        context["full_time_placements"] = queryset.filter(status="Full Time").count()
        context["part_time_placements"] = queryset.filter(status="Part Time").count()
        context["unique_physicians"] = (
            queryset.exclude(physician_id__isnull=True)
            .values("physician_id")
            .distinct()
            .count()
        )

        return context


class PlacementListView(LoginRequiredMixin, ListView):
    """List view for all placements with filtering."""

    model = Placement
    template_name = "dashboard/placement_list.html"
    context_object_name = "placements"
    paginate_by = 10  # Default to 10 rows per page

    def get_paginate_by(self, queryset):
        """Allow user to choose rows per page via query parameter."""
        # Get rows per page from query parameter, default to 10
        rows_per_page = self.request.GET.get("rows", "10")

        # Validate and set allowed values
        allowed_values = ["10", "25", "50", "100"]
        if rows_per_page not in allowed_values:
            rows_per_page = "10"

        # Store in session for persistence
        self.request.session["rows_per_page"] = rows_per_page

        return int(rows_per_page)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(physician_name__icontains=search)
                | Q(department__icontains=search)
                | Q(specialty__icontains=search)
                | Q(area__icontains=search)
            )

        return queryset.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")

        # Get current rows per page from session or request
        current_rows = self.request.GET.get(
            "rows", self.request.session.get("rows_per_page", "10")
        )
        context["current_rows"] = current_rows
        context["rows_options"] = [10, 25, 50, 100]

        return context


class PlacementCreateView(LoginRequiredMixin, CreateView):
    """Create view for new placements."""

    model = Placement
    form_class = PlacementForm
    template_name = "dashboard/placement_form.html"
    success_url = reverse_lazy("dashboard:placement_list")

    def form_valid(self, form):
        messages.success(self.request, "Placement created successfully!")
        return super().form_valid(form)


class PlacementUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for existing placements."""

    model = Placement
    form_class = PlacementForm
    template_name = "dashboard/placement_form.html"
    success_url = reverse_lazy("dashboard:placement_list")

    def form_valid(self, form):
        messages.success(self.request, "Placement updated successfully!")
        return super().form_valid(form)


class PlacementDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for placements."""

    model = Placement
    template_name = "dashboard/placement_confirm_delete.html"
    success_url = reverse_lazy("dashboard:placement_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Placement deleted successfully!")
        return super().delete(request, *args, **kwargs)


class PlacementDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a single placement."""

    model = Placement
    template_name = "dashboard/placement_detail.html"
    context_object_name = "placement"


@login_required
def analytics_data_api(request):
    """
    API endpoint for analytics data.
    Returns JSON data for charts based on filters.
    """
    # Base queryset
    queryset = Placement.objects.all()

    # Apply filters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    department = request.GET.get("department")
    specialty = request.GET.get("specialty")
    shift = request.GET.get("shift")
    status = request.GET.get("status")

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if department:
        queryset = queryset.filter(department=department)
    if specialty:
        queryset = queryset.filter(specialty=specialty)
    if shift:
        queryset = queryset.filter(shift=shift)
    if status:
        queryset = queryset.filter(status=status)

    # Department statistics - handle null values
    dept_stats = list(
        queryset.values("department").annotate(count=Count("id")).order_by("-count")
    )
    dept_stats = [
        {"department": stat["department"] or "Unknown", "count": stat["count"]}
        for stat in dept_stats
    ]

    # Specialty statistics - handle null values
    specialty_stats = list(
        queryset.values("specialty").annotate(count=Count("id")).order_by("-count")
    )
    specialty_stats = [
        {"specialty": stat["specialty"] or "Unknown", "count": stat["count"]}
        for stat in specialty_stats
    ]

    # Shift statistics - handle null values
    shift_stats = list(
        queryset.values("shift").annotate(count=Count("id")).order_by("shift")
    )
    shift_stats = [
        {"shift": stat["shift"] or "Unknown", "count": stat["count"]}
        for stat in shift_stats
    ]

    # Status statistics - handle null values
    status_stats = list(
        queryset.values("status").annotate(count=Count("id")).order_by("-count")
    )
    status_stats = [
        {"status": stat["status"] or "Unknown", "count": stat["count"]}
        for stat in status_stats
    ]

    # Time series data (last 30 days)
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)

    time_series = []
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        count = queryset.filter(date=date).count()
        time_series.append({"date": date.strftime("%Y-%m-%d"), "count": count})

    data = {
        "department_stats": dept_stats,
        "specialty_stats": specialty_stats,
        "shift_stats": shift_stats,
        "status_stats": status_stats,
        "time_series": time_series,
        "total_count": queryset.count(),
    }

    return JsonResponse(data)


# User CRUD Views - Admin Only
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """List view for all users with filtering. Admin only."""

    model = User
    template_name = "dashboard/user_list.html"
    context_object_name = "users"
    paginate_by = 10  # Default to 10 rows per page

    def test_func(self):
        """Only superusers can access user management."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect("dashboard:home")

    def get_paginate_by(self, queryset):
        """Allow user to choose rows per page via query parameter."""
        rows_per_page = self.request.GET.get("rows", "10")
        allowed_values = ["10", "25", "50", "100"]
        if rows_per_page not in allowed_values:
            rows_per_page = "10"
        self.request.session["rows_per_page"] = rows_per_page
        return int(rows_per_page)

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-date_joined")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        current_rows = self.request.GET.get(
            "rows", self.request.session.get("rows_per_page", "10")
        )
        context["current_rows"] = current_rows
        context["rows_options"] = [10, 25, 50, 100]
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create view for new users. Admin only."""

    model = User
    form_class = UserForm
    template_name = "dashboard/user_form.html"
    success_url = reverse_lazy("dashboard:user_list")

    def test_func(self):
        """Only superusers can create users."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        messages.error(self.request, "You don't have permission to create users.")
        return redirect("dashboard:home")

    def form_valid(self, form):
        messages.success(self.request, "User created successfully!")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update view for existing users. Admin only."""

    model = User
    form_class = UserForm
    template_name = "dashboard/user_form.html"
    success_url = reverse_lazy("dashboard:user_list")

    def test_func(self):
        """Only superusers can update users."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        messages.error(self.request, "You don't have permission to update users.")
        return redirect("dashboard:home")

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully!")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete view for users. Admin only."""

    model = User
    template_name = "dashboard/user_confirm_delete.html"
    success_url = reverse_lazy("dashboard:user_list")

    def test_func(self):
        """Only superusers can delete users."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        messages.error(self.request, "You don't have permission to delete users.")
        return redirect("dashboard:home")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User deleted successfully!")
        return super().delete(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Detail view for a single user. Admin only."""

    model = User
    template_name = "dashboard/user_detail.html"
    context_object_name = "user"

    def test_func(self):
        """Only superusers can view user details."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        messages.error(self.request, "You don't have permission to view user details.")
        return redirect("dashboard:home")


class ImportPlacementsView(LoginRequiredMixin, FormView):
    """View for importing placements from Excel file."""

    template_name = "dashboard/import_placements.html"
    form_class = ImportPlacementsForm
    success_url = reverse_lazy("dashboard:placement_list")

    def read_placements_excel(self, file_path):
        """Read placements from Excel file."""
        expected_columns = [
            "Date",
            "Shift",
            "Physician Name",
            "ID",
            "Department",
            "Speciality",
            "Status",
            "Area",
            "Room Number",
        ]

        with open(file_path, "rb") as f:
            _df = pd.read_excel(
                f,
                header=0,
                dtype=str,
                engine="openpyxl",
            )
        df = _df.where(pd.notnull(_df), None)

        # Map column names (case-insensitive, handle variations)
        column_mapping = {
            "date": "Date",
            "shift": "Shift",
            "physician name": "Physician Name",
            "physician_name": "Physician Name",
            "id": "ID",
            "department": "Department",
            "speciality": "Speciality",
            "specialty": "Speciality",
            "status": "Status",
            "area": "Area",
            "room number": "Room Number",
            "room_number": "Room Number",
        }

        # Rename columns if they don't match exactly
        df.columns = [
            column_mapping.get(col.strip().lower(), col) for col in df.columns
        ]

        # Ensure we have the expected columns (fill missing with None)
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        return df

    def form_valid(self, form):
        excel_file = form.cleaned_data["excel_file"]
        replace = form.cleaned_data["replace"]

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            for chunk in excel_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        try:
            # Clear existing data if replace is checked
            if replace:
                count = Placement.objects.count()
                Placement.objects.all().delete()
                messages.warning(
                    self.request,
                    f"Deleted {count} existing placements (replace mode)",
                )

            # Read Excel file
            df = self.read_placements_excel(tmp_file_path)

            # Process and import data
            created_count = 0
            skipped_count = 0
            error_count = 0

            for index, row in df.iterrows():
                try:
                    # Skip only if date, shift AND physician info are all missing
                    if (
                        pd.isna(row.get("Date"))
                        and pd.isna(row.get("Shift"))
                        and pd.isna(row.get("Physician Name"))
                    ):
                        skipped_count += 1
                        continue

                    # Prepare placement data
                    date_value = None
                    if pd.notna(row.get("Date")):
                        try:
                            date_obj = row.get("Date")
                            # If it's already a datetime/date object
                            if hasattr(date_obj, "date"):
                                date_value = date_obj.date()
                            elif isinstance(date_obj, str):
                                # Try multiple date formats
                                for fmt in [
                                    "%m/%d/%Y",
                                    "%m/%#d/%Y",
                                    "%Y-%m-%d",
                                    "%d/%m/%Y",
                                ]:
                                    try:
                                        date_value = datetime.strptime(
                                            date_obj.split(" ")[0], fmt
                                        ).date()
                                        break
                                    except:
                                        continue
                                # If string parsing failed, try pandas
                                if date_value is None:
                                    date_value = pd.to_datetime(
                                        date_obj, errors="coerce"
                                    )
                                    if pd.notna(date_value):
                                        date_value = date_value.date()
                            else:
                                # Try pandas to_datetime
                                date_value = pd.to_datetime(date_obj, errors="coerce")
                                if pd.notna(date_value):
                                    date_value = date_value.date()
                        except Exception as e:
                            logger.warning(f"Error parsing date: {e}")
                            date_value = None

                    placement_data = {
                        "date": date_value,
                        "shift": str(row.get("Shift")).strip()
                        if pd.notna(row.get("Shift"))
                        else None,
                        "physician_name": str(row.get("Physician Name")).strip()
                        if pd.notna(row.get("Physician Name"))
                        else None,
                        "physician_id": int(row.get("ID"))
                        if pd.notna(row.get("ID")) and str(row.get("ID")).strip() != ""
                        else None,
                        "department": str(row.get("Department")).strip()
                        if pd.notna(row.get("Department"))
                        else None,
                        "specialty": str(row.get("Speciality")).strip()
                        if pd.notna(row.get("Speciality"))
                        else None,
                        "status": str(row.get("Status")).strip()
                        if pd.notna(row.get("Status"))
                        else None,
                        "area": str(row.get("Area")).strip()
                        if pd.notna(row.get("Area"))
                        else None,
                        "room_number": str(row.get("Room Number")).strip()
                        if pd.notna(row.get("Room Number"))
                        else None,
                    }

                    # Create placement
                    Placement.objects.create(**placement_data)
                    created_count += 1

                except Exception as e:
                    logger.error(f"Error processing row {index}: {e}")
                    error_count += 1
                    skipped_count += 1

            # Success message
            messages.success(
                self.request,
                f"Import completed successfully! Created: {created_count}, "
                f"Skipped: {skipped_count}, Errors: {error_count}",
            )

        except Exception as e:
            logger.exception("Error importing placements")
            messages.error(self.request, f"Error importing placements: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

        return super().form_valid(form)


class DownloadTemplateView(LoginRequiredMixin, View):
    """View to download an empty Excel template for placements."""

    def get(self, request, *args, **kwargs):
        # Create an empty DataFrame with the required columns
        columns = [
            "Date",
            "Shift",
            "Physician Name",
            "ID",
            "Department",
            "Speciality",
            "Status",
            "Area",
            "Room Number",
        ]

        # Create empty DataFrame with column headers
        df = pd.DataFrame(columns=columns)

        # Add a few example rows to guide users
        example_rows = [
            {
                "Date": "11/30/2025",
                "Shift": "AM",
                "Physician Name": "John Doe",
                "ID": "12345",
                "Department": "IM",
                "Speciality": "INTERNAL MEDICINE",
                "Status": "Full Time",
                "Area": "MAIN",
                "Room Number": "A-8",
            },
            {
                "Date": "12/01/2025",
                "Shift": "PM",
                "Physician Name": "Jane Smith",
                "ID": "67890",
                "Department": "Cardiology",
                "Speciality": "CARDIOLOGY",
                "Status": "Part Time",
                "Area": "WING-B",
                "Room Number": "B-12",
            },
        ]

        # Add example rows
        df = pd.concat([df, pd.DataFrame(example_rows)], ignore_index=True)

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Placements")

            # Get the worksheet to format it
            worksheet = writer.sheets["Placements"]

            # Auto-adjust column widths
            try:
                from openpyxl.utils import get_column_letter

                for idx, col in enumerate(df.columns, 1):
                    max_length = max(df[col].astype(str).map(len).max(), len(col))
                    column_letter = get_column_letter(idx)
                    worksheet.column_dimensions[column_letter].width = min(
                        max_length + 2, 30
                    )
            except ImportError:
                # If openpyxl.utils is not available, skip column width adjustment
                pass

        output.seek(0)

        # Create HTTP response
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="placement_template.xlsx"'
        )

        return response


class ProfileView(LoginRequiredMixin, View):
    """View for user profile page."""

    template_name = "dashboard/profile.html"

    def get_context_data(self, **kwargs):
        context = kwargs.copy()
        context["user"] = self.request.user
        context["profile_form"] = kwargs.get(
            "profile_form", ProfileForm(instance=self.request.user)
        )
        context["password_form"] = kwargs.get(
            "password_form", PasswordChangeForm(user=self.request.user)
        )
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle profile updates."""
        if "update_profile" in request.POST:
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("dashboard:profile")
            else:
                context = self.get_context_data(profile_form=form)
                return render(request, self.template_name, context)
        elif "change_password" in request.POST:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Password changed successfully!")
                return redirect("dashboard:profile")
            else:
                context = self.get_context_data(password_form=form)
                return render(request, self.template_name, context)
        return redirect("dashboard:profile")


class SettingsView(LoginRequiredMixin, FormView):
    """View for application settings."""

    template_name = "dashboard/settings.html"
    form_class = SettingsForm
    success_url = reverse_lazy("dashboard:settings")

    def get_initial(self):
        """Get initial form values from session or defaults."""
        initial = super().get_initial()
        initial["theme"] = self.request.session.get("theme", "auto")
        initial["notifications"] = self.request.session.get("notifications", True)
        initial["email_notifications"] = self.request.session.get(
            "email_notifications", False
        )
        return initial

    def form_valid(self, form):
        """Save settings to session."""
        self.request.session["theme"] = form.cleaned_data["theme"]
        self.request.session["notifications"] = form.cleaned_data["notifications"]
        self.request.session["email_notifications"] = form.cleaned_data[
            "email_notifications"
        ]
        messages.success(self.request, "Settings saved successfully!")
        return super().form_valid(form)
