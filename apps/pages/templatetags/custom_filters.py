from django import template

register = template.Library()


@register.filter
def split(value, separator=","):
    """
    Split a string by a separator and return a list.
    Usage: {{ "a,b,c"|split:"," }}
    """
    if not value:
        return []
    return value.split(separator)
