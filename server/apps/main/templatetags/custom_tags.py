from django import template
# from django.contrib.auth.models import Group
from ..views import is_moderator
from django.template.defaultfilters import register
from urllib.parse import unquote 


register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.simple_tag
def toggle_story(val):
  if val == 1:
    return 'story'
  else:
    return 'stories'
  
register.simple_tag(is_moderator)  
  

@register.filter
def unquote_html(value):
    return unquote(value)
