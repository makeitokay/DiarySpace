from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, RedirectView, TemplateView

from diaryspace_auth import groups
from diaryspace_auth.forms import SchoolAdminCreationForm
from diaryspace_auth.models import User
from schools.models import School


class SchoolAdminCreationView(FormView):
    template_name = "diaryspace_auth/signup.html"
    form_class = SchoolAdminCreationForm
    success_url = "/"

    def form_valid(self, form):
        school = School.objects.create(
            region=form.cleaned_data["region"],
            city=form.cleaned_data["city"],
            school=form.cleaned_data["school"],
        )

        User.objects.create_school_admin(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            patronymic=form.cleaned_data["patronymic"],
            school_id=school.id,
        )
        form.send_registration_mail()

        return super().form_valid(form)


class UserHomeRedirect(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_admin:
            return "/admin"
        return reverse(groups.HOME_URLS[user.group.name])
