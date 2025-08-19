from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces a substring in the given value.
    Usage in template: {{ key|replace:"old,new" }}
    Example: {{ "hello_world"|replace:"_, " }} => "hello world"
    """
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except ValueError:
        return value
