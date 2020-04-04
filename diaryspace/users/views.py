from django.urls import reverse
from django.views.generic import FormView, TemplateView, RedirectView

from schools.models import School
from users.forms import SchoolAdminCreationForm
from users.models import User


class SchoolAdminCreationView(FormView):
    template_name = "signup.html"
    form_class = SchoolAdminCreationForm
    success_url = "/"

    def form_invalid(self, form):
        for error in form.errors:
            print(error)

        return super().form_invalid(form)

    def form_valid(self, form):
        region = form.cleaned_data["region"]
        city = form.cleaned_data["city"]
        school_name = form.cleaned_data["school"]
        school = School.objects.create(region=region, city=city, school=school_name)

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        name = form.cleaned_data["name"]
        surname = form.cleaned_data["surname"]
        patronymic = form.cleaned_data["patronymic"]

        User.objects.create_school_admin(
            email=email,
            password=password,
            name=name,
            surname=surname,
            patronymic=patronymic,
            school_id=school.id,
        )
        form.send_registration_mail()

        return super().form_valid(form)


class UserHomeRedirect(RedirectView):
    HOME_URLS = {
        'SchoolAdmin': 'announcements',
    }

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_admin:
            return '/admin'
        return reverse(self.HOME_URLS[user.role])

# class IndexView(TemplateView):
