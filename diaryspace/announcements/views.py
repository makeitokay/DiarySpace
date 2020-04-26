from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView

from announcements.forms import AnnouncementForm
from announcements.models import Announcement
from diaryspace_auth.mixins import SystemLoginRequiredMixin


class AnnouncementsView(SystemLoginRequiredMixin, ListView):
    template_name = "announcements/announcements.html"
    context_object_name = "announcements"

    def get_queryset(self):
        user = self.request.user
        return (
            user.group.announcement_set.filter(author__school=user.school)
            .order_by("-date_created")
            .select_related("author")
        )


class AnnouncementAddView(SystemLoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "announcements/announcement_add.html"
    form_class = AnnouncementForm
    success_url = reverse_lazy("announcements")
    permission_required = "announcements.add_announcement"

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.author = self.request.user
        announcement.save()

        # We can call `save_m2m` after `form.save(commit=False)`
        form.save_m2m()
        form.add_school_admin()

        return super().form_valid(form)


class AnnouncementEditView(
    SystemLoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    template_name = "announcements/announcement_edit.html"
    form_class = AnnouncementForm
    success_url = reverse_lazy("announcements")
    model = Announcement
    permission_required = "announcements.change_announcement"

    def has_permission(self):
        return (
            super().has_permission() and self.get_object().author == self.request.user
        )
