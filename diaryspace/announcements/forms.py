from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Div, Field
from django import forms
from django.contrib.auth.models import Group

from announcements.crispyforms_layouts import SubclassCustomizableSubmit
from announcements.models import Announcement
from diaryspace_auth import groups


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = (
            "title",
            "text",
            "groups",
        )
        widgets = {"text": forms.Textarea(), "groups": forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["groups"].queryset = self.fields["groups"].queryset.exclude(
            name=groups.SCHOOL_ADMIN
        )
        self.fields["groups"].required = False

        submit_button_text = "Создать"
        if kwargs.get("instance") is None:
            self.fields["groups"].initial = self.fields["groups"].queryset.values_list(
                "id", flat=True
            )
        else:
            submit_button_text = "Изменить"

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field("title", placeholder="Заголовок"),
                Field("text", placeholder="Текст"),
                Div(HTML("Объявление для групп пользователей:"), css_class="my-2"),
                Field("groups"),
            ),
            SubclassCustomizableSubmit(
                "submit",
                submit_button_text,
                css_class="btn-outline-primary create-announcement",
            ),
        )

    def save(self, commit=True):
        instance = super().save(commit)

        if commit:
            self.add_school_admin()

        return instance

    def add_school_admin(self):
        """Adds school admin to announcement groups (users who can view the announcement)"""
        school_admin_group = Group.objects.get(name=groups.SCHOOL_ADMIN)
        self.instance.groups.add(school_admin_group)
