"""
Placement model for clinic placement data.
"""

from django.db import models


class Placement(models.Model):
    """Model representing a clinic placement record."""

    # Shift choices
    SHIFT_AM = "AM"
    SHIFT_MD = "MD"
    SHIFT_PM = "PM"
    SHIFT_CLOSED = "CLOSED"

    SHIFT_CHOICES = [
        (SHIFT_AM, "Morning"),
        (SHIFT_MD, "Midday"),
        (SHIFT_PM, "Evening"),
        (SHIFT_CLOSED, "Closed"),
    ]

    STATUS_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
    ]

    # Fields based on Excel structure
    date = models.DateField(null=True, blank=True, help_text="Placement date")
    shift = models.CharField(
        max_length=10,
        choices=SHIFT_CHOICES,
        null=True,
        blank=True,
        help_text="Shift time (AM/MD/PM/CLOSED)",
    )
    physician_name = models.CharField(
        max_length=255, null=True, blank=True, help_text="Physician's full name"
    )
    physician_id = models.IntegerField(
        null=True, blank=True, help_text="Physician unique ID"
    )
    department = models.CharField(
        max_length=255, null=True, blank=True, help_text="Department name"
    )
    specialty = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Medical specialty",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        db_index=True,
        help_text="Placement status",
    )
    area = models.CharField(
        max_length=255, null=True, blank=True, help_text="Hospital area/wing"
    )
    room_number = models.CharField(
        max_length=50, null=True, blank=True, help_text="Room number"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "shift"]
        verbose_name = "Placement"
        verbose_name_plural = "Placements"
        indexes = [
            models.Index(fields=["-date", "shift"]),
            models.Index(fields=["department"]),
            models.Index(fields=["specialty"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        """String representation of the placement."""
        date_str = self.date.strftime("%Y-%m-%d") if self.date else "No Date"
        name = self.physician_name or "Unknown Physician"
        return f"{name} - {date_str} ({self.shift or 'N/A'})"

    @property
    def is_active(self):
        """Check if placement is currently active."""
        return self.status == self.STATUS_ACTIVE

    @classmethod
    def get_by_department(cls, department):
        """Get all placements for a specific department."""
        return cls.objects.filter(department=department)

    @classmethod
    def get_by_specialty(cls, specialty):
        """Get all placements for a specific specialty."""
        return cls.objects.filter(specialty=specialty)

    @classmethod
    def get_by_date_range(cls, start_date, end_date):
        """Get placements within a date range."""
        return cls.objects.filter(date__range=[start_date, end_date])

    @classmethod
    def get_statistics_by_department(cls):
        """Get placement count grouped by department."""
        from django.db.models import Count

        return (
            cls.objects.values("department")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @classmethod
    def get_statistics_by_specialty(cls):
        """Get placement count grouped by specialty."""
        from django.db.models import Count

        return (
            cls.objects.values("specialty")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @classmethod
    def get_statistics_by_shift(cls):
        """Get placement count grouped by shift."""
        from django.db.models import Count

        return cls.objects.values("shift").annotate(count=Count("id")).order_by("shift")

    @classmethod
    def get_statistics_by_status(cls):
        """Get placement count grouped by status."""
        from django.db.models import Count

        return (
            cls.objects.values("status").annotate(count=Count("id")).order_by("-count")
        )
