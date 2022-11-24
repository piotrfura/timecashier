from django import template
import datetime

register = template.Library()

@register.simple_tag
def count_signs(text):
    return len(text)
