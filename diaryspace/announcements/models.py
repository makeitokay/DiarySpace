from django.contrib.auth.models import Group
from django.db import models

from diaryspace.settings import AUTH_USER_MODEL


class Announcement(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="announcements")
    title = models.CharField(max_length=100)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group)  # groups of users who can see the announcement
