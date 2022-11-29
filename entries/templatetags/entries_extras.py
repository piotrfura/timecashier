from django import template

register = template.Library()


@register.simple_tag
def count_signs(text):
    return len(text)
