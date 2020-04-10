from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from schools.forms import AnnouncementForm
from users import groups


class AnnouncementsView(LoginRequiredMixin, ListView):
    template_name = "schools/announcements.html"
    context_object_name = "announcements"

    def get_queryset(self):
        user = self.request.user
        school = user.school
        return (
            user.group.announcement_set
                .filter(author__school=school)
                .order_by("-date_created")
                .select_related("author")
        )


class AnnouncementAddView(LoginRequiredMixin, FormView):
    template_name = "schools/announcement_add.html"
    form_class = AnnouncementForm
    success_url = reverse_lazy("announcements")

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.author = self.request.user
        announcement.save()

        # School admin can view all announcements, so we add him by default.
        for group in form.cleaned_data["groups"] | Group.objects.filter(name=groups.SCHOOL_ADMIN):
            announcement.groups.add(group)

        return super().form_valid(form)
