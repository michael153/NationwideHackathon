from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def getRange(value):
	return range(value)

def key(d, key_name):
	return d[key_name]
key = register.filter('key', key)
	
@register.filter
def index(List, i):
	return List[int(i)]