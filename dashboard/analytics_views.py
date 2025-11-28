"""
Additional analytics views for dedicated pages.
"""

import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from placements.models import Placement
from .forms import FilterForm
from datetime import datetime, timedelta


class DepartmentAnalyticsView(LoginRequiredMixin, TemplateView):
    """Dedicated page for department analytics."""

    template_name = "dashboard/analytics/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters (excluding department)
        filter_form = FilterForm(self.request.GET or None, exclude_field="department")
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters (all except department)
        if filter_form.is_valid():
            if filter_form.cleaned_data.get("start_date"):
                queryset = queryset.filter(
                    date__gte=filter_form.cleaned_data["start_date"]
                )
            if filter_form.cleaned_data.get("end_date"):
                queryset = queryset.filter(
                    date__lte=filter_form.cleaned_data["end_date"]
                )
            if filter_form.cleaned_data.get("specialty"):
                queryset = queryset.filter(
                    specialty=filter_form.cleaned_data["specialty"]
                )
            if filter_form.cleaned_data.get("shift"):
                queryset = queryset.filter(shift=filter_form.cleaned_data["shift"])
            if filter_form.cleaned_data.get("status"):
                queryset = queryset.filter(status=filter_form.cleaned_data["status"])

        # Department statistics - exclude null departments or mark them as "Unknown"
        dept_stats = list(
            queryset.values("department").annotate(count=Count("id")).order_by("-count")
        )

        # Process stats to handle null values
        processed_stats = []
        for stat in dept_stats:
            if stat["department"] is None:
                stat["department"] = "Unknown"
            processed_stats.append(stat)

        context["department_stats"] = processed_stats
        context["department_stats_json"] = json.dumps(processed_stats)
        context["total_placements"] = queryset.count()

        return context


class SpecialtyAnalyticsView(LoginRequiredMixin, TemplateView):
    """Dedicated page for specialty analytics."""

    template_name = "dashboard/analytics/specialty.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters (excluding specialty)
        filter_form = FilterForm(self.request.GET or None, exclude_field="specialty")
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters (all except specialty)
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
            if filter_form.cleaned_data.get("shift"):
                queryset = queryset.filter(shift=filter_form.cleaned_data["shift"])
            if filter_form.cleaned_data.get("status"):
                queryset = queryset.filter(status=filter_form.cleaned_data["status"])

        # Specialty statistics - exclude null specialties or mark them as "Unknown"
        specialty_stats = list(
            queryset.values("specialty").annotate(count=Count("id")).order_by("-count")
        )

        # Process stats to handle null values
        processed_stats = []
        for stat in specialty_stats:
            if stat["specialty"] is None:
                stat["specialty"] = "Unknown"
            processed_stats.append(stat)

        context["specialty_stats"] = processed_stats
        context["specialty_stats_json"] = json.dumps(processed_stats)
        context["total_placements"] = queryset.count()

        return context


class ShiftAnalyticsView(LoginRequiredMixin, TemplateView):
    """Dedicated page for shift analytics."""

    template_name = "dashboard/analytics/shifts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters (excluding shift)
        filter_form = FilterForm(self.request.GET or None, exclude_field="shift")
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters (all except shift)
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
            if filter_form.cleaned_data.get("status"):
                queryset = queryset.filter(status=filter_form.cleaned_data["status"])

        # Shift statistics - exclude null shifts or mark them as "Unknown"
        shift_stats = list(
            queryset.values("shift").annotate(count=Count("id")).order_by("shift")
        )

        # Process stats to handle null values
        processed_stats = []
        for stat in shift_stats:
            if stat["shift"] is None:
                stat["shift"] = "Unknown"
            processed_stats.append(stat)

        context["shift_stats"] = processed_stats
        context["shift_stats_json"] = json.dumps(processed_stats)
        context["total_placements"] = queryset.count()

        return context


class StatusAnalyticsView(LoginRequiredMixin, TemplateView):
    """Dedicated page for employment status analytics (Full Time/Part Time)."""

    template_name = "dashboard/analytics/status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters (excluding status)
        filter_form = FilterForm(self.request.GET or None, exclude_field="status")
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters (all except status)
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

        # Employment status statistics - exclude null statuses or mark them as "Unknown"
        status_stats = list(
            queryset.values("status").annotate(count=Count("id")).order_by("-count")
        )

        # Process stats to handle null values
        processed_stats = []
        for stat in status_stats:
            if stat["status"] is None:
                stat["status"] = "Unknown"
            processed_stats.append(stat)

        context["status_stats"] = processed_stats
        context["status_stats_json"] = json.dumps(processed_stats)
        context["total_placements"] = queryset.count()

        return context


class TimelineAnalyticsView(LoginRequiredMixin, TemplateView):
    """Dedicated page for timeline/trend analytics."""

    template_name = "dashboard/analytics/timeline.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters - exclude date filters since timeline shows dates
        filter_form = FilterForm(self.request.GET or None, exclude_field=None)
        # Remove date fields from the form since timeline is about dates
        if "start_date" in filter_form.fields:
            del filter_form.fields["start_date"]
        if "end_date" in filter_form.fields:
            del filter_form.fields["end_date"]
        context["filter_form"] = filter_form

        # Base queryset
        queryset = Placement.objects.all()

        # Apply filters (excluding date filters)
        department = self.request.GET.get("department")
        specialty = self.request.GET.get("specialty")
        shift = self.request.GET.get("shift")
        status = self.request.GET.get("status")

        if department:
            queryset = queryset.filter(department=department)
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        if shift:
            queryset = queryset.filter(shift=shift)
        if status:
            queryset = queryset.filter(status=status)

        # Time series data (last 30 days)
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)

        time_series = []
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            count = queryset.filter(date=date).count()
            time_series.append({"date": date.strftime("%Y-%m-%d"), "count": count})

        context["time_series"] = time_series
        context["time_series_json"] = json.dumps(time_series)
        context["total_placements"] = queryset.count()

        return context
