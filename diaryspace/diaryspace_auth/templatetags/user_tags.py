from django import template

_MANAGE_SCHOOL_PERMISSIONS = (
    "schools.change_school",
    "schools.change_schedule",
    "schools.change_callschedule",
    "schools.change_grade",
    "schools.change_subject",
)

_MANAGE_USERS_PERMISSIONS = (
    "users.add_parent",
    "users.add_student",
    "users.add_teacher",
)

register = template.Library()


@register.simple_tag
def can_manage_school(perms):
    return any(p in perms for p in _MANAGE_SCHOOL_PERMISSIONS)


@register.simple_tag
def can_manage_users(perms):
    return any(p in perms for p in _MANAGE_USERS_PERMISSIONS)
