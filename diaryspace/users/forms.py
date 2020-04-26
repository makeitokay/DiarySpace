from django import forms

from diaryspace_auth.forms import UserCreateForm
from schools.models import Grade, Subject
from users.models import Parent


class TeacherAddForm(UserCreateForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    homeroom_grade = forms.ModelChoiceField(
        queryset=Grade.objects.filter(homeroom_teacher=None), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter model choices to get only current school objects
        for field in ("subjects", "homeroom_grade"):
            self.fields[field].queryset = self.fields[field].queryset.filter(
                school_id=self.school_id
            )


class StudentAddForm(UserCreateForm):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=True)
    parent = forms.ModelChoiceField(queryset=Parent.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["grade"].queryset = self.fields["grade"].queryset.filter(
            school_id=self.school_id
        )
        self.fields["parent"].queryset = self.fields["parent"].queryset.filter(
            user__school_id=self.school_id
        )
