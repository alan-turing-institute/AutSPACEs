from django import template
from django.contrib.auth.models import Group

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
  
@register.simple_tag
def is_moderator(user):
  """return boolean if membership of moderator group"""
  
  try:
    group = Group.objects.get(user=user)
    return (group.name == "Moderators")
  
  except Group.DoesNotExist:
    return False

  
  
  