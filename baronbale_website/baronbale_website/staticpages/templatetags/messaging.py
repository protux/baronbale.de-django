from django import template
from django.contrib.sessions.models import Session

from baronbale_website.common import message_utils

register = template.Library()


@register.simple_tag
def get_error_messages(session: Session):
    return message_utils.get_error_messages(session)
