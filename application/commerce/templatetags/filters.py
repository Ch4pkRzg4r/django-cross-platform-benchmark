# commerce/templatetags/filters.py

from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Create a range up to the value provided."""
    return range(int(value))
