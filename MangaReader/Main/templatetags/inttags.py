from django.template import Library

register = Library()

def mark_count_formatter(value):
    if value > 1000:
        value = round(value / 1000, 1)
        if value == (r:=round(value)): 
            value = r
        return str(value) + 'К'
    else:
        return str(value)
    
register.filter('formatted_int', mark_count_formatter)