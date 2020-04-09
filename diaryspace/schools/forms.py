from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field, HTML, Button

from schools.models import Announcement


class AnnouncementForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Div(
            Field("title", placeholder="Заголовок"),
            Field("text", placeholder="Текст"),
            Div(HTML("Объявления для групп пользователей:"), css_class="my-2"),
            Field("groups"),
        ),
        Button(
            "submit",
            "Создать",
            type="submit",
            css_class="btn-outline-primary create-announcement"
        ),
    )

    class Meta:
        model = Announcement
        fields = ('title', 'text', 'groups',)
        widgets = {'text': forms.Textarea(), 'groups': forms.CheckboxSelectMultiple()}
