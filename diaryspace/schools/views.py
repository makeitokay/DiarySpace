from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from schools.forms import AnnouncementForm
from schools.models import Announcement


class AnnouncementsView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'announcements.html'
    form_class = AnnouncementForm
    context_object_name = 'announcements'
    success_url = 'announcements'

    def get_queryset(self):
        group = Group.objects.get(name=self.request.user.role)
        return group.announcement_set.order_by('-date_created')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.school = request.user.school
            announcement.author = request.user
            announcement.save()

            for group in form.cleaned_data['groups']:
                announcement.groups.add(group)
            announcement.save()

            return redirect(self.get_success_url())

        return self.get(request, args, kwargs)
