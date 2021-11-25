from django.template.defaulttags import register


@register.filter
def division(value1, value2):
    return value1 / value2


@register.filter
def multi(value1, value2):
    return value1 * value2
