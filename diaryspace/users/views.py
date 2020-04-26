from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from diaryspace_auth import groups
from diaryspace_auth.forms import UserCreateForm
from diaryspace_auth.mixins import SystemLoginRequiredMixin
from diaryspace_auth.models import User
from users.forms import TeacherAddForm, StudentAddForm
from users.models import Teacher, Parent, Student


class UserListView(SystemLoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        school = self.request.user.school
        return (
            self.model.objects.filter(user__school=school).select_related("user").all()
        )


class UserAddView(SystemLoginRequiredMixin, PermissionRequiredMixin, FormView):
    group_name = None

    def create_user(self, form):
        random_password = User.objects.make_random_password()
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=random_password,
            school_id=self.request.user.school_id,
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            patronymic=form.cleaned_data["patronymic"],
            group_name=self.group_name,
        )
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"school_id": self.request.user.school_id})
        return kwargs


class TeacherListView(UserListView):
    template_name = "users/teacher_list.html"
    context_object_name = "teachers"
    permission_required = "users.view_teacher"
    model = Teacher


class TeacherAddView(UserAddView):
    template_name = "users/teacher_add.html"
    permission_required = "users.add_teacher"
    form_class = TeacherAddForm
    success_url = reverse_lazy("teachers")
    group_name = groups.TEACHER

    def form_valid(self, form):
        user = self.create_user(form)

        teacher = Teacher.objects.create(
            user=user, homeroom_grade=form.cleaned_data["homeroom_grade"]
        )
        for subject in form.cleaned_data["subjects"]:
            teacher.subjects.add(subject)

        return super().form_valid(form)


class ParentListView(UserListView):
    template_name = "users/parent_list.html"
    context_object_name = "parents"
    permission_required = "users.view_parent"
    model = Parent


class ParentAddView(UserAddView):
    template_name = "users/parent_add.html"
    permission_required = "users.add_parent"
    form_class = UserCreateForm
    success_url = reverse_lazy("parents")
    group_name = groups.PARENT

    def form_valid(self, form):
        user = self.create_user(form)
        Parent.objects.create(user=user)

        return super().form_valid(form)


class StudentListView(UserListView):
    template_name = "users/student_list.html"
    context_object_name = "students"
    permission_required = "users.view_student"
    model = Student


class StudentAddView(UserAddView):
    template_name = "users/student_add.html"
    permission_required = "users.add_student"
    form_class = StudentAddForm
    success_url = reverse_lazy("students")
    group_name = groups.STUDENT

    def form_valid(self, form):
        user = self.create_user(form)

        student = Student.objects.create(
            user=user,
            parent=form.cleaned_data["parent"],
            grade=form.cleaned_data["grade"],
        )

        return super().form_valid(form)
