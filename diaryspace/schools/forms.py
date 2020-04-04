from django import forms

from schools.models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'text', 'groups',)
        widgets = {'groups': forms.CheckboxSelectMultiple}
