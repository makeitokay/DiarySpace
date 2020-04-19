from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from diaryspace_auth import groups
from diaryspace_auth.mixins import SystemLoginRequiredMixin
from diaryspace_auth.models import User
from users.forms import TeacherAddForm
from users.models import Teacher


class TeacherListView(SystemLoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'users/teacher_list.html'
    context_object_name = 'teachers'
    permission_required = 'users.view_teacher'

    def get_queryset(self):
        school = self.request.user.school
        return Teacher.objects.filter(user__school=school).select_related('user').all()


class TeacherAddView(SystemLoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'users/teacher_add.html'
    permission_required = 'users.add_teacher'
    form_class = TeacherAddForm
    success_url = reverse_lazy('teachers')

    def form_valid(self, form):
        random_password = User.objects.make_random_password()
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=random_password,
            school_id=self.request.user.school_id,
            name=form.cleaned_data['name'],
            surname=form.cleaned_data['surname'],
            patronymic=form.cleaned_data['patronymic'],
            group_name=groups.TEACHER
        )

        teacher = Teacher.objects.create(
            user=user,
            homeroom_grade=form.cleaned_data['homeroom_grade']
        )
        for subject in form.cleaned_data['subjects']:
            teacher.subjects.add(subject)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add school id to form to get subjects choices
        kwargs.update({"school_id": self.request.user.school_id})
        return kwargs
