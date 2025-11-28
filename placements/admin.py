"""
Admin configuration for Placement model.
"""

from django.contrib import admin
from .models import Placement


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    """Admin interface for Placement model."""

    list_display = [
        "physician_name",
        "date",
        "shift",
        "department",
        "specialty",
        "status",
        "area",
        "room_number",
    ]

    list_filter = [
        "date",
        "shift",
        "department",
        "specialty",
        "status",
        "area",
    ]

    search_fields = [
        "physician_name",
        "physician_id",
        "department",
        "specialty",
        "area",
        "room_number",
    ]

    list_per_page = 50

    date_hierarchy = "date"

    fieldsets = (
        ("Physician Information", {"fields": ("physician_name", "physician_id")}),
        ("Placement Details", {"fields": ("date", "shift", "status")}),
        ("Location", {"fields": ("department", "specialty", "area", "room_number")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        """Optimize queryset with select_related if needed."""
        qs = super().get_queryset(request)
        return qs
