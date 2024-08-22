from django import template
from accounts.models import CustomUserModel
from agents.models import AgentCustomUserModel

register = template.Library()

@register.filter
def is_user(user):
    return isinstance(user, CustomUserModel)

@register.filter
def is_agent_user(user):
    return isinstance(user, AgentCustomUserModel)

