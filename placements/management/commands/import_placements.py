"""
Django management command to import placement data from Excel file.
Usage: python manage.py import_placements --replace
"""

from datetime import datetime
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from placements.models import Placement
import logging

logger = logging.getLogger(__name__)


def read_placements_excel(file_path):
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
    with open(file_path, "rb") as f:
        _df = pd.read_excel(
            f,
            header=0,
            dtype=str,
            engine="openpyxl",
            parse_dates=["Date"],
            date_format="%m/%#d/%Y",
        )
    df = _df.where(pd.notnull(_df), None)
    df.columns = columns
    return df


class Command(BaseCommand):
    help = "Import clinic placement data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="Copy of clinic placment dashboard.xlsx",
            help="Path to the Excel file (relative to project root)",
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing placements (clear all before importing)",
        )

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / options["file"]

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # Clear existing data if requested
        if options["replace"]:
            count = Placement.objects.count()
            Placement.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Deleted {count} existing placements (replace mode)"
                )
            )

        try:
            # Read Excel file
            self.stdout.write(f"Reading Excel file: {file_path}")
            df = read_placements_excel(file_path)

            # Log column names
            self.stdout.write(f"Found columns: {df.columns.tolist()}")
            self.stdout.write(f"Total rows in file: {len(df)}")

            # Process and import data
            created_count = 0
            skipped_count = 0

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
                    placement_data = {
                        "date": row.get("Date").split(" ")[0]
                        if pd.notna(row.get("Date"))
                        else None,
                        "shift": str(row.get("Shift")).strip()
                        if pd.notna(row.get("Shift"))
                        else None,
                        "physician_name": str(row.get("Physician Name")).strip()
                        if pd.notna(row.get("Physician Name"))
                        else None,
                        "physician_id": int(row.get("ID"))
                        if pd.notna(row.get("ID"))
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

                    # Create placement (simple create, no update_or_create to avoid duplicates)
                    Placement.objects.create(**placement_data)
                    created_count += 1

                except Exception as e:
                    logger.error(f"Error processing row {index}: {e}")
                    self.stdout.write(self.style.WARNING(f"Skipped row {index}: {e}"))
                    skipped_count += 1

            # Summary
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nImport completed:\n"
                    f"  - Created: {created_count}\n"
                    f"  - Skipped: {skipped_count}\n"
                    f"  - Total in database: {Placement.objects.count()} placements"
                )
            )

        except Exception as e:
            logger.exception("Error importing placements")
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
