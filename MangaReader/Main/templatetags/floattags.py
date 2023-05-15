from django.template.defaultfilters import floatformat 
from django.template import Library

register = Library()

def formatted_float(value):
    value = round(value, 2)
    if value == round(value):
        value = round(value)
    return str(value)


register.filter('formatted_float', formatted_float)