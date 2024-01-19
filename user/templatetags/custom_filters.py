from django import template 

register = template.Library()

@register.filter(name='sub')
def subtract(first_value, second_value): 
    return first_value - second_value 

@register.filter(name='add')
def sum_value(first_value, second_value): 
    return first_value + second_value 