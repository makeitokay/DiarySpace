from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from diaryspace_auth import groups
from diaryspace_auth.mixins import SystemLoginRequiredMixin
from diaryspace_auth.models import User
from users.forms import TeacherAddForm
from users.models import Teacher


class UserListView(SystemLoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        school = self.request.user.school
        return self.model.objects.filter(user__school=school).select_related('user').all()


class UserAddView(SystemLoginRequiredMixin, PermissionRequiredMixin, FormView):
    group_name = None

    def create_user(self, form):
        random_password = User.objects.make_random_password()
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=random_password,
            school_id=self.request.user.school_id,
            name=form.cleaned_data['name'],
            surname=form.cleaned_data['surname'],
            patronymic=form.cleaned_data['patronymic'],
            group_name=self.group_name
        )
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"school_id": self.request.user.school_id})
        return kwargs


class TeacherListView(UserListView):
    template_name = 'users/teacher_list.html'
    context_object_name = 'teachers'
    permission_required = 'users.view_teacher'
    model = Teacher


class TeacherAddView(UserAddView):
    template_name = 'users/teacher_add.html'
    permission_required = 'users.add_teacher'
    form_class = TeacherAddForm
    success_url = reverse_lazy('teachers')
    group_name = groups.TEACHER

    def form_valid(self, form):
        user = self.create_user(form)

        teacher = Teacher.objects.create(
            user=user,
            homeroom_grade=form.cleaned_data['homeroom_grade']
        )
        for subject in form.cleaned_data['subjects']:
            teacher.subjects.add(subject)

        return super().form_valid(form)
