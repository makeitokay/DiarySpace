_MANAGE_SCHOOL_PERMISSIONS = (
    'schools.change_school',
    'schools.change_schedule',
    # TODO: расписание звонков
    'schools.change_grade',
    'schools.change_subject'
)

_MANAGE_USERS_PERMISSIONS = (
    'users.add_parent',
    'users.add_student',
    'users.add_teacher'
)


def can_user_manage_school(request):
    return {
        'can_user_manage_school': any(request.user.has_perm(p) for p in _MANAGE_SCHOOL_PERMISSIONS)
    }


def can_user_manage_users(request):
    return {
        'can_user_manage_users': any(request.user.has_perm(p) for p in _MANAGE_USERS_PERMISSIONS)
    }