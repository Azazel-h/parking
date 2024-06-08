from django import template

register = template.Library()


@register.filter
def add_hour(value):
    try:
        hour = int(value)
        next_hour = (hour + 1) % 24
        return "{:02d}:00".format(next_hour)
    except (ValueError, TypeError):
        return value
