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

# for keeping toggles while moving between pagination pages
# idea is to replace only the page number in the url, keep the rest
@register.simple_tag
def url_replace(request, field, value):
    """Replace or add a specific query parameter to the current request's url"""
    query = request.GET.copy()
    query[field] = value
    return '?{}'.format(query.urlencode())
