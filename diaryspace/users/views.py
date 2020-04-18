from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from diaryspace_auth.mixins import SystemLoginRequiredMixin
from users.models import Teacher


class TeacherListView(SystemLoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'users/teacher_list.html'
    context_object_name = 'teachers'
    permission_required = 'users.view_teacher'

    def get_queryset(self):
        school = self.request.user.school
        return Teacher.objects.filter(user__school=school).all()
