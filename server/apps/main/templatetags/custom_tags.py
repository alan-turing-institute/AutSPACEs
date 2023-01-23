from django import template
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