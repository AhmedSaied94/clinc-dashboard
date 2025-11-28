"""
Custom template filters for analytics calculations.
"""

from django import template

register = template.Library()


@register.filter
def percentage(value, total):
    """Calculate percentage with proper handling of edge cases."""
    if not value or not total or total == 0:
        return 0
    try:
        percentage_value = (float(value) / float(total)) * 100
        return round(percentage_value, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def safe_percentage(value, total):
    """Calculate percentage and format as string with % symbol, handling edge cases."""
    if not value or not total or total == 0:
        return "0%"
    try:
        percentage_value = (float(value) / float(total)) * 100
        return f"{round(percentage_value, 2)}%"
    except (ValueError, TypeError, ZeroDivisionError):
        return "0%"

