from django import forms

from schools.models import Announcement

from .widgets import BootstrapCheckboxSelectMultiple


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'text', 'groups',)
        widgets = {'groups': BootstrapCheckboxSelectMultiple}
