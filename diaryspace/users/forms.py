from django import forms

from diaryspace_auth.forms import UserCreateForm
from schools.models import Grade, Subject


class TeacherAddForm(UserCreateForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    homeroom_grade = forms.ModelChoiceField(
        queryset=Grade.objects.filter(homeroom_teacher=None), required=False
    )

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop("school_id")
        super().__init__(*args, **kwargs)

        # Filter model choices to get only current school objects
        for field in ("subjects", "homeroom_grade"):
            self.fields[field].queryset = self.fields[field].queryset.filter(
                school_id=school_id
            )
