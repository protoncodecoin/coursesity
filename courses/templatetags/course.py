from django import template

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter(name="range")
def get_range(value):
    return range(value)
