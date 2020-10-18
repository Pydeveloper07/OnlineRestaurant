from django import template

register = template.Library()

@register.filter
def times(count):
    return range(1, int(count+1))

@register.filter
def access(value, arg):
    return value[arg]