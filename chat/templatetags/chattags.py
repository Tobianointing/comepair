from django import template


register = template.Library()

@register.simple_tag
def get_other_user(user, object):
    if object.first != user:
        return object.first
    return object.second