from django import template


register = template.Library()

UNITS = {
    'px': 1.0,
    'pt': 1.0,
    'in': 72.0,
    'mm': 0.0393700787 * 72
}


@register.filter
def normalize_unit(value, unit):
    if value < 0:
        return 0
    return value * UNITS[unit]
