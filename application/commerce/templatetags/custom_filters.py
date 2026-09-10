# commerce/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def times(value):
    """Returns a range object for a given value."""
    try:
        return range(int(value))  # Convert value to integer and return a range
    except (TypeError, ValueError):
        return []
# commerce/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    return value.split(delimiter)

# commerce/templatetags/filters.py

from django import template

register = template.Library()

@register.filter
def range_filter(value):
    try:
        value = int(value) if value is not None else 0  # Handle None by using 0 as default
        return range(value)
    except ValueError:
        return range(0)
    
    # commerce/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Splits the input string by the provided key.
    Usage: {{ value|split:"," }}
    """
    return value.split(key)



