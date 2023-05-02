from django import template

register = template.Library()

@register.filter
def filter_by_tag(files, tag):
    return [file for file in files if tag in file['metadata']['tags']]

@register.filter
def filter_by_moderation_status(files, status):
    return [file for file in files if file['metadata']['data']['moderation_status'] == status]
